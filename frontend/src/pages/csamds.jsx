import { useSearchParams } from "react-router-dom";

import BaseLayout from "@/components/layouts/BaseLayout";
import { Separator } from "@/components/ui/separator";
import DescriptiveHeader from "@/components/static/descriptive-header";
import SummaryBar from "@/features/summary-bar/SummaryBar";
import SummaryTable from "@/features/summary-table/SummaryTable";
import { cn } from "@/lib/utils";

const CsamDS = () => {
  const [searchParams] = useSearchParams();
  const method = searchParams.get("method");

  return (
    <BaseLayout
      className={cn(
        "flex flex-col",
        method === "train" ? "bg-yellow-100" : "bg-sky-100",
      )}
    >
      <div className="flex py-2">
        <DescriptiveHeader
          className="w-2/3"
          title="CSAM Dataset Preview"
          description="Overall dataset summary for CSAM Model Training."
        />
        <Separator orientation="vertical" className="bg-slate-400" />
        <div className="flex w-1/3">
          <SummaryBar method={method} />
        </div>
      </div>
      <Separator className="px-4" />
      <SummaryTable method={method} />
    </BaseLayout>
  );
};

export default CsamDS;
