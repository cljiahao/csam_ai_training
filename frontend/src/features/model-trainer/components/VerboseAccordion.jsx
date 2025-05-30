import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
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

  return (
    <Accordion
      className="no-scrollbar hw-full overflow-y-auto rounded-xl"
      type="single"
      collapsible
    >
      <AccordionItem className="bg-white px-4" value="item-1">
        <AccordionTrigger>
          {status === STATUS.IDLE
            ? "Press the Train button to start"
            : status === "processing"
              ? "Augmenting in progress..."
              : (mainContent ?? "Training in progress...")}
        </AccordionTrigger>
        <AccordionContent className="flex flex-col">
          {remainderContent.map((data, index) => {
            return <span key={index}>{data}</span>;
          })}
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  );
};

export default VerboseAccordion;
