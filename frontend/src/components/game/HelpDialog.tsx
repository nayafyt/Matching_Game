import { useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";
import { cn } from "@/lib/cn";

interface Props {
  open: boolean;
  onClose: () => void;
}

export function HelpDialog({ open, onClose }: Props) {
  const { t } = useTranslation();
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const el = dialogRef.current;
    if (!el) return;
    if (open && !el.open) el.showModal();
    if (!open && el.open) el.close();
  }, [open]);

  return (
    <dialog
      ref={dialogRef}
      onClose={onClose}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
      className={cn(
        "fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2",
        "rounded-2xl border border-border bg-card text-card-foreground p-0 shadow-xl",
        "w-[min(32rem,90vw)] max-h-[90vh] overflow-y-auto",
        "backdrop:bg-foreground/40 backdrop:backdrop-blur-sm",
      )}
    >
      <div className="p-6 space-y-5">
        <div className="flex items-start justify-between gap-4">
          <h2 className="text-xl font-semibold">{t("help.title")}</h2>
          <button
            type="button"
            onClick={onClose}
            aria-label={t("help.close")}
            className="rounded-full h-10 w-10 inline-flex items-center justify-center text-2xl leading-none text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
          >
            ×
          </button>
        </div>

        <Section title={t("help.matchTitle")} body={t("help.matchBody")} />
        <Section title={t("help.scoringTitle")} body={t("help.scoringBody")} />
        <Section title={t("help.specialTitle")} body={t("help.specialBody")} />
        <Section title={t("help.endTitle")} body={t("help.endBody")} />
      </div>
    </dialog>
  );
}

function Section({ title, body }: { title: string; body: string }) {
  return (
    <div>
      <h3 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground mb-1">
        {title}
      </h3>
      <p className="text-sm leading-relaxed">{body}</p>
    </div>
  );
}
