import type { ToastMessageOptions } from "primevue/toast";
import type { ToastServiceMethods } from "primevue/toastservice";

type toast = ToastMessageOptions & {
  meta: { level?: string };
};

function message(detail: string, level?: string): toast {
  return {
    life: 1000,
    detail,
    severity: "custom",
    meta: { level },
  };
}

export function showtoast(
  toast: ToastServiceMethods,
  detail: string,
  level?: "success" | "info" | "warn" | "error",
) {
  toast.add(message(detail, level || "success"));
}

export function showtoastsuccess(toast: ToastServiceMethods, t: (key: string) => string) {
  showtoast(toast, t("Success"), "success");
}

export function showtoasterror(toast: ToastServiceMethods, t: (key: string) => string) {
  showtoast(toast, t("Error"), "error");
}
