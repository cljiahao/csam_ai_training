import BaseLayout from "@/components/layouts/BaseLayout";
import { Separator } from "@/components/ui/separator";
import DescriptiveHeader from "@/components/static/descriptive-header";
import UtilityPanel from "@/features/settings-bar/components/UtilityPanel";
import SummaryTable from "@/features/summary-table/SummaryTable";

const CsamDS = () => {
  return (
    <BaseLayout className="flex flex-col bg-yellow-100">
      <div className="flex py-2">
        <DescriptiveHeader
          className="w-2/3"
          title="CSAM Dataset Preview"
          description="Overall dataset summary for CSAM Model Training."
        />
        <Separator orientation="vertical" className="bg-slate-400" />
        <UtilityPanel className="w-1/3" />
      </div>
      <Separator className="px-4" />
      <SummaryTable />
    </BaseLayout>
  );
};

export default CsamDS;
