import { useEffect } from "react";
import { io } from "socket.io-client";
import { useQueryClient } from "@tanstack/react-query";

export default function LiveUpdater() {
  const qc = useQueryClient();

  useEffect(() => {
    const socket = io(import.meta.env.VITE_API_WS || "");
    socket.on("metrics", (m: any) => {
      qc.setQueryData(["metrics"], m);
      qc.setQueryData(["mapLatest"], m);
      qc.setQueryData(["heatmap"], m);
    });
    return () => { socket.disconnect(); };
  }, [qc]);

  return null;
}
