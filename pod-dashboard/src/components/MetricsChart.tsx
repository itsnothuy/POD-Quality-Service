import { useQuery } from "@tanstack/react-query";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, Legend,
  PieChart, Pie, Cell
} from "recharts";

interface Rate { timestamp: string; blur_rate: number; underlit_rate: number; }
interface Metrics {
  rates: Rate[];
  latest: { blurry: number; underlit: number }[];
}

export default function MetricsChart() {
  const { data } = useQuery<Metrics>({
    queryKey: ["metrics"],
    queryFn: () => fetch("/metrics/json").then(r => r.json()),
    refetchInterval: 30_000,
  });

  if (!data) return <div>Loading…</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <LineChart width={600} height={300} data={data.rates}>
        <XAxis dataKey="timestamp" />
        <YAxis />
        <Line dataKey="blur_rate" strokeWidth={2} />
        <Line dataKey="underlit_rate" strokeWidth={2} />
        <Tooltip />
        <Legend />
      </LineChart>

      <PieChart width={300} height={300}>
        <Pie
          data={data.latest}
          dataKey="value"
          nameKey="name"
          outerRadius={100}
          label
        >
          <Cell key="blur" name="Blurry" fill="#8884d8" />
          <Cell key="light" name="Underlit" fill="#82ca9d" />
        </Pie>
        <Tooltip />
      </PieChart>
    </div>
  );
}
