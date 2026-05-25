import { useTranslation } from "react-i18next";
import { Button } from "@/components/ui/button";

export function LanguageToggle() {
  const { i18n, t } = useTranslation();
  const current = i18n.resolvedLanguage ?? "en";
  const next = current === "en" ? "el" : "en";

  return (
    <Button
      variant="outline"
      size="sm"
      onClick={() => void i18n.changeLanguage(next)}
      aria-label={t("language")}
    >
      {current === "en" ? "EN" : "EL"} → {next === "en" ? "EN" : "EL"}
    </Button>
  );
}
