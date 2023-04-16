export const baseUrl = import.meta.env.DEV
  ? "http://web:8000"
  : "http://webserver:80";

export const imageBaseUrl = import.meta.env.DEV
  ? "http://web:8000"
  : "http://0.0.0.0:1337";
