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
      <div className="grid grid-cols-2 gap-2 overflow-hidden">
        {evalResults?.results.map((evalResult) => (
          <Accordion key={evalResult?.mode} type="single" collapsible>
            <AccordionItem value="item-1">
              <AccordionTrigger>{`${evalResult?.mode} - Number of Outflows: ${evalResult?.outflows?.length}`}</AccordionTrigger>
              <AccordionContent
                style={{
                  height: `${window.innerHeight / 2}px`,
                  overflowY: "auto",
                }}
                className="grid grid-cols-5"
              >
                {evalResult?.outflows?.length ? (
                  evalResult.outflows.map((file_src) => {
                    const fileName = file_src.split("\\").pop();
                    return (
                      <MediaCard
                        key={file_src}
                        className="p-1 text-xs hover:bg-slate-100 2xl:text-sm"
                        title={fileName}
                        descClassName=""
                      >
                        <img
                          className="w-[60%]"
                          src={`/api/csam_image/${file_src}`}
                          alt={fileName}
                        />
                      </MediaCard>
                    );
                  })
                ) : (
                  <div className="flex-center col-span-5 py-16 text-lg font-semibold text-gray-500">
                    No Outflows found
                  </div>
                )}
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        ))}
      </div>
    </CustomDialog>
  );
};

export default EvalOutflow;
