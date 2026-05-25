import { useState } from "react";
import { useTranslation } from "react-i18next";
import { HelpDialog } from "./HelpDialog";

export function HelpButton() {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label={t("help.open")}
        title={t("help.open")}
        className="h-8 w-8 inline-flex items-center justify-center rounded-full border border-border bg-secondary text-secondary-foreground font-semibold text-sm hover:bg-accent hover:text-accent-foreground transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      >
        ?
      </button>
      <HelpDialog open={open} onClose={() => setOpen(false)} />
    </>
  );
}
