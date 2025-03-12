import { useSearchParams } from "react-router-dom";

import BaseLayout from "@/components/layouts/BaseLayout";
import DescriptiveHeader from "@/components/static/descriptive-header";
import { Separator } from "@/components/ui/separator";
import ModelBar from "@/features/model-bar/ModelBar";
import ModelTrainer from "@/features/model-trainer/ModelTrainer";
import EvaluationResults from "@/features/evaluation-results/EvaluationResults";

const CsamMT = () => {
  const [searchParams] = useSearchParams();
  const item = searchParams.get("item");
  const method = searchParams.get("method");

  // TODO: If item or method don't exists, re-direct to CDS
  // TODO: check if item exists in backend database.
  // TODO: if model train completed, show sweetalert

  return (
    <BaseLayout
      className={`flex flex-col ${method === "train" ? "bg-yellow-100" : "bg-lime-100"}`}
    >
      <div className="flex py-2">
        <DescriptiveHeader
          className="w-2/3"
          title={
            method === "train"
              ? "CSAM Model Training"
              : "Re-training CSAM Model"
          }
          description={`Currently ${method.toLowerCase()}ing model for ${item}.`}
        />
        <Separator orientation="vertical" />
        <ModelBar className="w-1/3" item={item} />
      </div>
      <Separator className="px-4" />
      <div className="flex min-h-0 flex-1">
        <ModelTrainer className="w-2/3" item={item} />
        <EvaluationResults className="w-1/3" item={item} />
      </div>
    </BaseLayout>
  );
};

export default CsamMT;
