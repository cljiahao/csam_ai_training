import { FaHome } from "react-icons/fa";
import { TbTableSpark } from "react-icons/tb";
import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { IoMdSettings } from "react-icons/io";

// Information for different sections or pages with descriptions
const navigation_info = [
  {
    name: "Home",
    url: "/",
    title: "Home Page",
    description: "Home Page",
    icon: FaHome,
    component: "Home",
  },
  {
    name: "CDS",
    url: "/CDS",
    title: "CSAM Dataset Summary",
    description: "Checklist of CSAM dataset summary for CSAM Model Training.",
    icon: TbTableSpark,
    component: "CsamDS",
  },
  {
    name: "CMT",
    url: "/CMT",
    title: "CSAM Model Training",
    description:
      "Website for training AI models and evaluating models accuracy using evaluation points.",
    icon: LiaChalkboardTeacherSolid,
    component: "CsamMT",
  },
  {
    name: "Settings",
    url: "/Settings",
    title: "Settings",
    description: "Configurations webpage for user to edit parameters.",
    icon: IoMdSettings,
    component: "Settings",
  },
];

export { navigation_info };
