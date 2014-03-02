using System;

namespace Mygod.Musicript.Instruments.Waves
{
    /// <summary>
    /// 正弦波。
    /// </summary>
    public sealed class SineWave
    {
        /// <summary>
        /// 取样。
        /// </summary>
        /// <param name="time">当前时刻。（单位：秒）</param>
        /// <returns>返回范围在 [-1, 1] 之间的样本。</returns>
        public double Sample(double time)
        {
            return Math.Sin(2 * Math.PI * time);
        }
    }
    /// <summary>
    /// 方波。
    /// </summary>
    public sealed class SquareWave
    {
        /// <summary>
        /// 取样。
        /// </summary>
        /// <param name="time">当前时刻。（单位：秒）</param>
        /// <returns>返回范围在 [-1, 1] 之间的样本。</returns>
        public double Sample(double time)
        {
            time -= Math.Floor(time);
            time = Math.Floor(time + time);
            return time + time - 1;
        }
    }
    /// <summary>
    /// 三角波。
    /// </summary>
    public sealed class TriangleWave
    {
        /// <summary>
        /// 取样。
        /// </summary>
        /// <param name="time">当前时刻。（单位：秒）</param>
        /// <returns>返回范围在 [-1, 1] 之间的样本。</returns>
        public double Sample(double time)
        {
            time -= Math.Floor(time);
            time = Math.Abs(time + time - 1);
            return time + time - 1;
        }
    }
    /// <summary>
    /// 锯齿波。
    /// </summary>
    public sealed class SawtoothWave
    {
        /// <summary>
        /// 取样。
        /// </summary>
        /// <param name="time">当前时刻。（单位：秒）</param>
        /// <returns>返回范围在 [-1, 1] 之间的样本。</returns>
        public double Sample(double time)
        {
            time -= Math.Floor(time);
            return time + time - 1;
        }
    }
    /// <summary>
    /// 抛物波。
    /// </summary>
    public sealed class ParabolicWave
    {
        /// <summary>
        /// 取样。
        /// </summary>
        /// <param name="time">当前时刻。（单位：秒）</param>
        /// <returns>返回范围在 [-1, 1] 之间的样本。</returns>
        public double Sample(double time)
        {
            time -= Math.Floor(time) + 0.5;
            return 1 - 8 * time * time;
        }
    }
    /// <summary>
    /// 平滑抛物波。
    /// </summary>
    public sealed class SmoothParabolicWave
    {
        /// <summary>
        /// 取样。
        /// </summary>
        /// <param name="time">当前时刻。（单位：秒）</param>
        /// <returns>返回范围在 [-1, 1] 之间的样本。</returns>
        public double Sample(double time)
        {
            time -= Math.Floor(time) + 0.5;
            var temp = Math.Abs(time);
            return (time * (1 - temp - temp)) * 8;
        }
    }
    /// <summary>
    /// 白噪声。
    /// </summary>
    public sealed class WhiteNoise
    {
        private readonly Random random = new Random();

        /// <summary>
        /// 取样。
        /// </summary>
        /// <param name="time">当前时刻。（单位：秒）</param>
        /// <returns>返回范围在 [-1, 1] 之间的样本。</returns>
        public double Sample(double time)
        {
            time = random.NextDouble();
            return time + time - 1;
        }
    }
}
