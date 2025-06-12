import { useMap } from "react-leaflet";
import HeatmapLayer from "react-leaflet-heatmap-layer-v3";
import { useQuery } from "@tanstack/react-query";

export default function HeatmapView() {
  const { data } = useQuery<{ latest: { lat: number; lon: number }[] }>({
    queryKey: ["heatmap"],
    queryFn: () => fetch("/metrics/json").then(r => r.json()),
    refetchInterval: 30_000,
  });

  const map = useMap();
  if (!data) return null;

  const points = data.latest.map(d => [d.lat, d.lon, 0.5]);
  return <HeatmapLayer fitBoundsOnLoad points={points} map={map} />;
}
