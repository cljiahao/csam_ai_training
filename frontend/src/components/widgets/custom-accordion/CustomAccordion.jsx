import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const CustomAccordion = ({ children, label, itemValue, heightFactor }) => {
  return (
    <Accordion type="single" collapsible>
      <AccordionItem value={itemValue}>
        <AccordionTrigger>{label}</AccordionTrigger>
        <AccordionContent
          style={{
            height: heightFactor
              ? `${window.innerHeight / heightFactor}px`
              : "auto",
            overflowY: "auto",
          }}
          className="hw-full"
        >
          {children}
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  );
};

export default CustomAccordion;
