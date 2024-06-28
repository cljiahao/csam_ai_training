import React from "react";

import Input from "../../../../../../common/components/Input";
import Upload from "../../../../../../common/components/Upload";
import Button from "../../../../../../common/components/Button";

const UploadSave = ({ upload_info, input_info, button_info }) => {
  return (
    <div className="grid h-full w-full grid-cols-5">
      <div>
        <Upload name="upload" upload_info={upload_info} />
      </div>
      <div className="col-span-3 text-base 2xl:text-lg">
        <Input name="item" input_info={input_info} />
      </div>
      <div>
        <Button name="save" button_info={button_info} />
      </div>
    </div>
  );
};

export default UploadSave;
