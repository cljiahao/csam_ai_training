import Swal from "sweetalert2";
import { useSearchParams } from "react-router-dom";
import { useShallow } from "zustand/react/shallow";

import BaseLayout from "@/components/layouts/BaseLayout";
import DescriptiveHeader from "@/components/static/descriptive-header";
import { Separator } from "@/components/ui/separator";
import ModelBar from "@/features/model-bar/ModelBar";
import ModelTrainer from "@/features/model-trainer/ModelTrainer";
import EvaluationResults from "@/features/evaluation-results/EvaluationResults";
import { cn } from "@/lib/utils";
import useBaseStore from "@/store/base";
import useTrainStore from "@/store/train";
import { METHOD_PARAMS } from "@/constants/url-params";
import { STATUS } from "@/constants/common";

const CsamMT = () => {
  const [searchParams] = useSearchParams();
  const item = searchParams.get("item");
  const method = searchParams.get("method") || METHOD_PARAMS.TRAIN;

  // TODO: If item or method don't exists, re-direct to CDS
  // TODO: check if item exists in backend database.

  const error = useBaseStore((state) => state.error);
  const resetError = useBaseStore((state) => state.resetError);
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  if (error) {
    updateStatus(STATUS.IDLE);
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: error,
    }).then((result) => {
      if (result.isConfirmed) {
        resetError();
      }
    });
  }

  // Check for completed status
  const isCompleted = status === STATUS.EVALUATED;

  if (isCompleted)
    Swal.fire({
      icon: "success",
      title: `Model ${method === METHOD_PARAMS.TRAIN ? "Training" : "Retraining"} Completed`,
      text: "Please check if there are any Outflows before installing.",
    });

  return (
    <BaseLayout
      className={cn(
        "flex flex-col",
        method === METHOD_PARAMS.TRAIN ? "bg-yellow-100" : "bg-sky-100",
      )}
    >
      <div className="flex py-2">
        <DescriptiveHeader
          className="w-2/3"
          title={
            method === METHOD_PARAMS.TRAIN
              ? "CSAM Model Training"
              : "Re-training CSAM Model"
          }
          description={`Currently ${method === METHOD_PARAMS.TRAIN ? "training" : "retraining"} model for ${item}.`}
        />
        <Separator orientation="vertical" />
        <ModelBar className="w-1/3" item={item} method={method} />
      </div>
      <Separator className="px-4" />
      <div className="flex min-h-0 flex-1">
        <ModelTrainer className="w-2/3" item={item} method={method} />
        <EvaluationResults className="w-1/3" item={item} method={method} />
      </div>
    </BaseLayout>
  );
};

export default CsamMT;
