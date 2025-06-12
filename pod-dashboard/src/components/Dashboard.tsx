import MapView from "./MapView";
import MetricsChart from "./MetricsChart";
export default function Dashboard() {
  return (
    <div className="space-y-8">
      <MetricsChart />
      <MapView />
      {/* Map and heatmap go here */}
      
    </div>
  );
}
