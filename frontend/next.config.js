/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/backend/:path*",
        destination: "https://ai-social-content-maker-api.onrender.com/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
