using System;

namespace Mygod.Musicript.Instruments.Waves
{
    /// <summary>
    /// 正弦波。
    /// </summary>
    public static class SineWave
    {
        /// <summary>
        /// 取样。
        /// </summary>
        /// <param name="time">当前时刻。（单位：秒）</param>
        /// <returns>返回范围在 [-1, 1] 之间的样本。</returns>
        public static double Sample(double time)
        {
            return Math.Sin(2 * Math.PI * time);
        }
    }
    /// <summary>
    /// 方波。
    /// </summary>
    public static class SquareWave
    {
        /// <summary>
        /// 取样。
        /// </summary>
        /// <param name="time">当前时刻。（单位：秒）</param>
        /// <returns>返回范围在 [-1, 1] 之间的样本。</returns>
        public static double Sample(double time)
        {
            time += time;
            var temp = Math.Floor(time);
            temp += temp - Math.Floor(time + time);
            return temp + temp + 1;
        }
    }
    /// <summary>
    /// 三角波。
    /// </summary>
    public static class TriangleWave
    {
        /// <summary>
        /// 取样。
        /// </summary>
        /// <param name="time">当前时刻。（单位：秒）</param>
        /// <returns>返回范围在 [-1, 1] 之间的样本。</returns>
        public static double Sample(double time)
        {
            time %= 1;
            var temp = Math.Abs(time + time - 1);
            return temp + temp - 1;
        }
    }
    /// <summary>
    /// 锯齿波。
    /// </summary>
    public static class SawtoothWave
    {
        /// <summary>
        /// 取样。
        /// </summary>
        /// <param name="time">当前时刻。（单位：秒）</param>
        /// <returns>返回范围在 [-1, 1] 之间的样本。</returns>
        public static double Sample(double time)
        {
            var temp = time - Math.Floor(time);
            return temp + temp - 1;
        }
    }
}
