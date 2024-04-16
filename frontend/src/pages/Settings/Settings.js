import React, { useState } from "react";
import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { PiGauge } from "react-icons/pi";

import NavBar from "../../common/components/NavBar";
import Menu from "../../common/containers/Menu/Menu";

const Settings = () => {
  const [menu, setMenu] = useState(false);

  const openMenu = async () => {
    setMenu(!menu);
  };

  const button_info = {
    train: {
      name: "Train",
      icon: <LiaChalkboardTeacherSolid />,
      style: { font: "text-3xl" },
      onClick: () => (window.location.href = "/"),
    },
    evaluate: {
      name: "Evaluate",
      icon: <PiGauge />,
      style: { font: "text-3xl" },
      onClick: () => (window.location.href = "/"),
    },
  };
  return (
    <main className="flex h-screen w-screen bg-amber-100">
      <section className="w-full">test</section>
      <aside className="relative w-[60%] border-l-2 border-slate-400">
        <NavBar openMenu={openMenu} button_info={button_info} />
        <Menu openMenu={openMenu} menu={menu} />
      </aside>
    </main>
  );
};

export default Settings;
