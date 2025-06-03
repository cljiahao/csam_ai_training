import CustomAccordion from "@/components/widgets/custom-accordion/CustomAccordion";
import { STATUS } from "@/constants/common";

const VerboseAccordion = ({ epoch_data, status }) => {
  const accordionData =
    epoch_data
      ?.slice()
      .reverse()
      .map(
        ({
          time,
          epoch,
          total_epoch,
          accuracy,
          val_accuracy,
          loss,
          val_loss,
        }) =>
          `time: ${time}s, epoch: ${epoch}/${total_epoch}, accuracy: ${accuracy}, val_accuracy: ${val_accuracy}, loss: ${loss}, val_loss: ${val_loss}`,
      ) ?? [];

  const [mainContent, ...remainderContent] = accordionData;
  const label =
    status === STATUS.IDLE
      ? "Press the Train button to start"
      : status === "processing"
        ? "Augmenting in progress..."
        : (mainContent ?? "Training in progress...");

  return (
    <div className="hw-full no-scrollbar overflow-y-auto rounded-xl bg-white px-4">
      <CustomAccordion label={label} itemValue="item-1">
        <div className="flex flex-col">
          {remainderContent.map((data, index) => {
            return <span key={index}>{data}</span>;
          })}
        </div>
      </CustomAccordion>
    </div>
  );
};

export default VerboseAccordion;
