import { MdCompare } from "react-icons/md";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

import CustomDialog from "@/components/widgets/custom-dialog/CustomDialog";
import HoverButton from "@/components/widgets/hover-button/HoverButton";
import MediaCard from "@/components/widgets/media-card/MediaCard";
import useOutflow from "../hooks/useOutflow";

const EvalOutflow = ({ disabled }) => {
  const {
    state: { isDialogOpen, evalResults },
    action: { handleDialogOpen },
  } = useOutflow();

  return (
    <CustomDialog
      className="h-[95%] w-[95%] max-w-screen-3xl"
      trigger={
        <HoverButton
          icon={MdCompare}
          hoverText="Outflows"
          className="w-24 text-lg"
          disabled={disabled}
        />
      }
      title={"Outflows / Fake Good"}
      description="Outflows from Trained Model Evaluation."
      open={isDialogOpen}
      onOpenChange={handleDialogOpen}
    >
      <div className="grid grid-cols-2 gap-2">
        {evalResults?.results.map((evalResult) => (
          <Accordion key={evalResult?.mode} type="single" collapsible>
            <AccordionItem value="item-1">
              <AccordionTrigger>{`${evalResult?.mode} - Number of Outflows: ${evalResult?.cm_results?.false_neg}`}</AccordionTrigger>
              <AccordionContent className="grid grid-cols-5">
                {evalResult?.outflows?.map((file_src) => {
                  const fileName = file_src.split("\\").pop();
                  return (
                    <MediaCard
                      key={file_src}
                      className="hover:bg-slate-100"
                      title={fileName}
                      description="Outflow"
                      descClassName="pb-2"
                    >
                      {<img src={`/api/image/${file_src}`} alt={fileName} />}
                    </MediaCard>
                  );
                })}
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        ))}
      </div>
    </CustomDialog>
  );
};

export default EvalOutflow;
