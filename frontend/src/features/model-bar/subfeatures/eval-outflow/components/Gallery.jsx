import MediaCard from "@/components/widgets/media-card/MediaCard";

const Gallery = ({ outflows }) => {
  if (!outflows || outflows.length == 0) {
    return (
      <div className="flex-center hw-full text-lg font-semibold text-gray-500">
        No Outflows found
      </div>
    );
  }

  return (
    <div className="hw-full grid grid-cols-5">
      {outflows.map((file_src) => {
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
      })}
    </div>
  );
};

export default Gallery;
