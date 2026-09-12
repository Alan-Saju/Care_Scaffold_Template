import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import { API } from "@/utils/api";

const STATUS_LABELS = {
  draft: "connect__status_draft",
  scheduled: "connect__status_scheduled",
  in_progress: "connect__status_in_progress",
  completed: "connect__status_completed",
  cancelled: "connect__status_cancelled",
} as const;

export default function ConsultationsPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const facility = new URLSearchParams(window.location.search).get("facility") ?? "";
  const [title, setTitle] = useState("");
  const [scheduledAt, setScheduledAt] = useState("");

  const consultations = useQuery({
    queryKey: ["care_connect", "consultations", facility],
    queryFn: () => API.consultations(facility || undefined),
  });
  const create = useMutation({
    mutationFn: () =>
      API.createConsultation({
        facility,
        title: title.trim(),
        status: scheduledAt ? "scheduled" : "draft",
        scheduled_at: scheduledAt ? new Date(scheduledAt).toISOString() : null,
      }),
    onSuccess: () => {
      setTitle("");
      setScheduledAt("");
      void queryClient.invalidateQueries({
        queryKey: ["care_connect", "consultations"],
      });
    },
  });

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-6">
      <div>
        <h1 className="text-xl font-bold">{t("connect__page_title")}</h1>
        <p className="mt-1 text-sm text-secondary-700">
          {t("connect__page_description")}
        </p>
      </div>
      <form
        className="space-y-3 rounded-lg border border-secondary-300 bg-white p-4 shadow-sm"
        onSubmit={(event) => {
          event.preventDefault();
          if (facility && title.trim()) create.mutate();
        }}
      >
        <h2 className="font-semibold">{t("connect__new_consultation")}</h2>
        <input
          required
          className="h-9 w-full rounded-md border border-secondary-400 px-3 text-sm"
          placeholder={t("connect__title_placeholder")}
          value={title}
          onChange={(event) => setTitle(event.target.value)}
        />
        <input
          className="h-9 w-full rounded-md border border-secondary-400 px-3 text-sm"
          type="datetime-local"
          value={scheduledAt}
          onChange={(event) => setScheduledAt(event.target.value)}
        />
        <Button type="submit" size="sm" disabled={!facility || create.isPending}>
          {create.isPending
            ? t("connect__saving")
            : t("connect__create_consultation")}
        </Button>
        {!facility && (
          <p className="text-sm text-red-600">{t("connect__facility_required")}</p>
        )}
      </form>
      <section className="space-y-3">
        <h2 className="font-semibold">{t("connect__consultations")}</h2>
        {consultations.isLoading && (
          <p className="text-sm text-secondary-700">{t("connect__loading")}</p>
        )}
        {consultations.error && (
          <p className="text-sm text-red-600">{t("connect__load_error")}</p>
        )}
        {consultations.data?.map((consultation) => (
          <article
            className="rounded-lg border border-secondary-300 bg-white p-4"
            key={consultation.external_id}
          >
            <div className="flex items-center justify-between gap-4">
              <h3 className="font-semibold">{consultation.title}</h3>
              <span className="rounded-full bg-primary-100 px-2 py-1 text-xs text-primary-800">
                {t(STATUS_LABELS[consultation.status])}
              </span>
            </div>
            {consultation.scheduled_at && (
              <p className="mt-2 text-sm text-secondary-700">
                {new Date(consultation.scheduled_at).toLocaleString()}
              </p>
            )}
          </article>
        ))}
        {!consultations.isLoading && !consultations.data?.length && (
          <p className="text-sm text-secondary-700">{t("connect__empty")}</p>
        )}
      </section>
    </div>
  );
}
