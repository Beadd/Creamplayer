import { defineStore } from "pinia";
import { ref } from "vue";

export const useLoginStore = defineStore("login", () => {
  const neteaseCookie = ref("");

  const login = () => {
    (window as any).electron.invoke("netease-login");
  };

  const get = async () => {
    const res = await (window as any).electron.invoke("get-netease-login");
    if (res) {
      neteaseCookie.value = res;
      return true;
    } else {
      return false;
    }
  };

  return {
    login,
    get,
    neteaseCookie,
  };
});
