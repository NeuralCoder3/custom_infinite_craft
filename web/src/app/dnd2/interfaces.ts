

export interface Note {
  id: string;
  content: string | null;
  image?: string;
  position: {
    x: number;
    y: number;
  };
}