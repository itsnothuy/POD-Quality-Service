import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Dashboard from "./components/Dashboard";

const qc = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={qc}>
      <div className="p-4">
        <h1 className="text-2xl font-bold mb-4">POD Dashboard</h1>
        <Dashboard />
      </div>
    </QueryClientProvider>
  );
}