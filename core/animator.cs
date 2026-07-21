using System;
using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Media.Imaging;
using System.Windows.Interop;

namespace LuminaAnimator
{
    public class AnimatorApp : Application
    {
        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);

        [DllImport("user32.dll", SetLastError = true)]
        public static extern IntPtr SendMessageTimeout(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam, uint fuFlags, uint uTimeout, out IntPtr lpdwResult);

        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);
        public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern IntPtr FindWindowEx(IntPtr parentHandle, IntPtr childAfter, string className, string windowTitle);

        [DllImport("user32.dll", SetLastError = true)]
        public static extern IntPtr SetParent(IntPtr hWndChild, IntPtr hWndNewParent);

        [DllImport("user32.dll", SetLastError = true)]
        public static extern bool SystemParametersInfo(uint uiAction, uint uiParam, string pvParam, uint fWinIni);

        private static IntPtr workerw = IntPtr.Zero;

        [STAThread]
        public static void Main(string[] args)
        {
            if (args.Length < 2) return;
            string oldWall = args[0];
            string newWall = args[1];
            string style = args.Length > 2 ? args[2] : "circle";

            IntPtr progman = FindWindow("Progman", null);
            IntPtr result = IntPtr.Zero;
            SendMessageTimeout(progman, 0x052C, IntPtr.Zero, IntPtr.Zero, 0x0000, 1000, out result);

            EnumWindows(new EnumWindowsProc((tophandle, topparamhandle) =>
            {
                IntPtr p = FindWindowEx(tophandle, IntPtr.Zero, "SHELLDLL_DefView", null);
                if (p != IntPtr.Zero)
                {
                    workerw = FindWindowEx(IntPtr.Zero, tophandle, "WorkerW", null);
                }
                return true;
            }), IntPtr.Zero);

            if (workerw == IntPtr.Zero) return;

            AnimatorApp app = new AnimatorApp();
            Window win = new Window
            {
                WindowStyle = WindowStyle.None,
                AllowsTransparency = true,
                Background = Brushes.Transparent,
                ShowInTaskbar = false,
                Left = 0,
                Top = 0,
                Width = SystemParameters.PrimaryScreenWidth,
                Height = SystemParameters.PrimaryScreenHeight,
                Topmost = false,
                ResizeMode = ResizeMode.NoResize
            };

            Grid grid = new Grid();

            try {
                Image oldImg = new Image { Source = new BitmapImage(new Uri(oldWall, UriKind.Absolute)), Stretch = Stretch.UniformToFill };
                grid.Children.Add(oldImg);
            } catch {}

            Image newImg = null;
            try {
                newImg = new Image { Source = new BitmapImage(new Uri(newWall, UriKind.Absolute)), Stretch = Stretch.UniformToFill };
                grid.Children.Add(newImg);
            } catch {}

            if (newImg == null) return;

            if (style.ToLower() == "circle")
            {
                EllipseGeometry clipGeo = new EllipseGeometry
                {
                    Center = new Point(win.Width / 2, win.Height / 2),
                    RadiusX = 0,
                    RadiusY = 0
                };
                newImg.Clip = clipGeo;

                double maxRadius = Math.Sqrt(Math.Pow(win.Width, 2) + Math.Pow(win.Height, 2));

                DoubleAnimation animX = new DoubleAnimation(0, maxRadius, TimeSpan.FromSeconds(1)) { EasingFunction = new CircleEase { EasingMode = EasingMode.EaseOut } };
                DoubleAnimation animY = new DoubleAnimation(0, maxRadius, TimeSpan.FromSeconds(1)) { EasingFunction = new CircleEase { EasingMode = EasingMode.EaseOut } };

                animX.Completed += (s, e) => { SetFinalAndExit(newWall); };

                win.Loaded += (s, e) =>
                {
                    IntPtr hwnd = new WindowInteropHelper(win).Handle;
                    SetParent(hwnd, workerw);
                    clipGeo.BeginAnimation(EllipseGeometry.RadiusXProperty, animX);
                    clipGeo.BeginAnimation(EllipseGeometry.RadiusYProperty, animY);
                };
            }
            else
            {
                newImg.Opacity = 0;
                DoubleAnimation anim = new DoubleAnimation(0, 1, TimeSpan.FromSeconds(1));
                anim.Completed += (s, e) => { SetFinalAndExit(newWall); };

                win.Loaded += (s, e) =>
                {
                    IntPtr hwnd = new WindowInteropHelper(win).Handle;
                    SetParent(hwnd, workerw);
                    newImg.BeginAnimation(UIElement.OpacityProperty, anim);
                };
            }

            win.Content = grid;
            win.Show();
            app.Run();
        }

        private static void SetFinalAndExit(string path)
        {
            SystemParametersInfo(20, 0, path, 3);
            Environment.Exit(0);
        }
    }
}
