import { VideoIcon } from "lucide-react";
import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";

import Page from "./Page";

/**
 * Implements the `FacilityHomeActions` extension point.
 * Props mirror `care_fe/src/pluginTypes.ts` — only the fields used are declared.
 */
export default function FacilityHomeActions({
  facility,
  className,
}: {
  facility: { id: string };
  className?: string;
}) {
  const { t } = useTranslation();

  return (
    <Page>
      <Button asChild variant="primary" size="sm" className={className}>
        <a href={`/connect?facility=${encodeURIComponent(facility.id)}`}>
          <VideoIcon />
          {t("connect__action_label")}
        </a>
      </Button>
    </Page>
  );
}
