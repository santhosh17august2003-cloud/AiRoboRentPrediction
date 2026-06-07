const localApiUrl =
  typeof window !== "undefined" && window.location.hostname === "localhost"
    ? "http://127.0.0.1:5000"
    : "https://ai-robo-rent-prediction.vercel.app";

const API_BASE_URL = (process.env.REACT_APP_API_URL || localApiUrl).replace(
  /\/$/,
  ""
);

export function apiUrl(path) {
  return `${API_BASE_URL}${path}`;
}
