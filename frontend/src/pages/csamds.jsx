import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

import BaseLayout from "@/components/layouts/BaseLayout";
import { Separator } from "@/components/ui/separator";
import DescriptiveHeader from "@/components/static/descriptive-header";
import UtilityPanel from "@/features/settings-bar/components/UtilityPanel";
import SummaryTable from "@/features/summary-table/SummaryTable";
import { cn } from "@/lib/utils";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";

const CsamDS = () => {
  const [isChecked, setChecked] = useState(false);
  const [searchParams] = useSearchParams();
  const method = searchParams.get("method");

  const navigate = useNavigate();
  useEffect(() => {
    if (!method || method != "retrain") {
      setChecked(false);
      navigate(`/CDS?method=train`);
    } else {
      setChecked(true);
    }
  }, [method, navigate]);

  const onCheckChange = (checkState) => {
    if (checkState) navigate(`/CDS?method=retrain`);
    else navigate(`/CDS?method=train`);
    setChecked(checkState);
  };

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
        <div className="flex w-1/3 gap-12">
          <UtilityPanel className="w-1/6" />
          <div className="flex w-5/6 items-center gap-6">
            <Switch
              id="model-method"
              checked={isChecked}
              onCheckedChange={onCheckChange}
            />
            <Label htmlFor="model-method" className="text-2xl capitalize">
              {method}
            </Label>
          </div>
        </div>
      </div>
      <Separator className="px-4" />
      <SummaryTable method={method} />
    </BaseLayout>
  );
};

export default CsamDS;
