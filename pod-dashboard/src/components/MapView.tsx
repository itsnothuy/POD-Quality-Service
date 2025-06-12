import { MapContainer, TileLayer, CircleMarker } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useQuery } from "@tanstack/react-query";
import HeatmapView from "./HeatmapLayer";

interface Delivery {
  id: string;
  lat: number;
  lon: number;
}

export default function MapView() {
  const { data } = useQuery<{ latest: Delivery[] }>({
    queryKey: ["mapLatest"],
    queryFn: () => fetch("/metrics/json").then(r => r.json()),
    refetchInterval: 30_000,
  });

  if (!data) return <div>Loading map…</div>;

  return (
    <MapContainer center={[37.77, -122.42]} zoom={12} className="h-80 w-full">
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {data.latest.map(d => (
        <CircleMarker
          key={d.id}
          center={[d.lat, d.lon]}
          radius={6}
          className="fill-red-500 stroke-none"
        />
      ))}
      <HeatmapView/>
    </MapContainer>
  );
}
