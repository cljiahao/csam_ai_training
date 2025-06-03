import CustomAccordion from "@/components/widgets/custom-accordion/CustomAccordion";
import CustomDialog from "@/components/widgets/custom-dialog/CustomDialog";
import Gallery from "./components/Gallery";
import useOutflow from "./hooks/useOutflow";

const EvalOutflow = ({ triggerChildren }) => {
  const {
    state: { isDialogOpen, evalResults },
    action: { handleDialogOpen },
  } = useOutflow();

  return (
    <CustomDialog
      className="h-[95%] w-[95%] max-w-screen-3xl"
      trigger={triggerChildren}
      title="Outflows / Fake Good"
      description="Outflows from Trained Model Evaluation."
      open={isDialogOpen}
      onOpenChange={handleDialogOpen}
    >
      {evalResults ? (
        <div className="no-scrollbar grid grid-cols-2 gap-2 overflow-y-auto">
          {evalResults?.results.map(({ mode, outflows }) => {
            const label = `${mode} - Number of Outflows: ${outflows?.length}`;
            return (
              <CustomAccordion
                key={mode}
                label={label}
                itemValue={mode}
                heightFactor={Math.ceil(evalResults?.results?.length / 2)}
              >
                <Gallery outflows={outflows} />
              </CustomAccordion>
            );
          })}
        </div>
      ) : (
        <div className="hw-full flex-center text-xl italic">
          Please Start Train and Evaluate to see Outflows.
        </div>
      )}
    </CustomDialog>
  );
};

export default EvalOutflow;
