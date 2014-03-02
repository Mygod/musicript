using System;

namespace Mygod.Musicript.Interpolators.Inflection
{
    /// <summary>
    /// 线性变调插值。
    /// </summary>
    public sealed class LinearInflection
    {
        private static double speed;

        /// <summary>
        /// 设置变调速度。
        /// </summary>
        /// <param name="value"></param>
        public void SetSpeed(string value)
        {
            speed = double.Parse(value);
        }

        /// <summary>
        /// 插值。
        /// </summary>
        /// <param name="frequency">原频率。</param>
        /// <param name="time">时刻。</param>
        /// <returns>插值后映射到的时刻。</returns>
        public double Interpolate(double frequency, double time)
        {
            var result = time * (frequency + speed * time / 2);
            if (speed >= 0) return result;
            var temp = -frequency / speed;
            return time > temp ? temp * frequency / 2 : result;
        }
    }

    /// <summary>
    /// 对数变调插值。
    /// </summary>
    public sealed class LogarithmicInflection
    {
        private static double speed;

        /// <summary>
        /// 设置变调速度。
        /// </summary>
        /// <param name="value"></param>
        public void SetSpeed(string value)
        {
            speed = double.Parse(value);
        }

        /// <summary>
        /// 插值。
        /// </summary>
        /// <param name="frequency">原频率。</param>
        /// <param name="time">时刻。</param>
        /// <returns>插值后映射到的时刻。</returns>
        public double Interpolate(double frequency, double time)
        {
            if (Math.Abs(speed) < 1e-8) return frequency * time;
                                        // no inflection
            return frequency * (Math.Exp(speed * time) - 1) / speed;
        }
    }
}
