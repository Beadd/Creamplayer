import { defineStore } from "pinia";

export const useLoginStore = defineStore("login", () => {
  const login = () => {
    (window as any).electron.invoke("open");
  };

  return {
    login,
  };
});
