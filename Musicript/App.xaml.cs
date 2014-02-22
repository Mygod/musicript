using System;
using System.IO;
using System.Reflection;
using System.Threading;
using System.Windows;
using System.Windows.Threading;

namespace Mygod.Musicript
{
    public sealed partial class App
    {
        static App()
        {
            AppDomain.CurrentDomain.UnhandledException += OnUnhandledException;
            AppDomain.CurrentDomain.SetData("PRIVATE_BINPATH", "Resources\\Libraries");
            var m = typeof(AppDomainSetup).GetMethod("UpdateContextProperty", BindingFlags.NonPublic | BindingFlags.Static);
            var fusion = typeof(AppDomain).GetMethod("GetFusionContext", BindingFlags.NonPublic | BindingFlags.Instance);
            m.Invoke(null, new[] { fusion.Invoke(AppDomain.CurrentDomain, null), "PRIVATE_BINPATH", "Bin" });
        }

        private static void OnUnhandledException(object sender, UnhandledExceptionEventArgs e)
        {
            OnError(e.ExceptionObject as Exception);
        }

        private void OnUnhandledException(object sender, DispatcherUnhandledExceptionEventArgs e)
        {
            e.Handled = true;
            OnError(e.Exception);
        }

        private static void OnError(Exception e)
        {
            if (e == null || e is ThreadAbortException) return;
            var msg = e.GetMessage();
            File.AppendAllText("crash.log", msg + Environment.NewLine);
            MessageBox.Show("貌似这个程序发生了某种未知错误。以下是详细信息。为了解决此问题，请将目录下的 crash.log 发给作者。(mygod.tk)"
                            + Environment.NewLine + msg, "ERROR", MessageBoxButton.OK, MessageBoxImage.Error);
            Current.Shutdown();
        }
    }
}
