export type ConsultationStatus =
  | "draft"
  | "scheduled"
  | "in_progress"
  | "completed"
  | "cancelled";

export interface Consultation {
  external_id: string;
  facility: string;
  title: string;
  status: ConsultationStatus;
  scheduled_at: string | null;
  notes: string;
  provider_reference: string;
  created_date: string;
}

export interface ConsultationInput {
  facility: string;
  title: string;
  status?: ConsultationStatus;
  scheduled_at?: string | null;
}
