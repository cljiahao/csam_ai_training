import { toast } from "@/hooks/use-toast";

const showUploadToast = ({ mode, item, fileName, targetCount }) => {
  toast({
    title: `You submitted the following values for ${mode}:`,
    description: (
      <pre className="mt-2 flex w-[340px] flex-col rounded-md bg-slate-950 p-4">
        <kbd className="text-white">Item Type: {item}</kbd>
        <kbd className="text-white">File Name: {fileName}</kbd>
        <kbd className="text-white">Target Count: {targetCount}</kbd>
      </pre>
    ),
    duration: 2000,
  });
};

export default showUploadToast;
