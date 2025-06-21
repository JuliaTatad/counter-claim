"use client"

import { useState } from "react"
import { Button } from "./components/ui/button"
import CausationChain from "./causation-chain"
import StrategyDashboard from "./strategy-dashboard"
import CaseLawMatrix from "./case-law-matrix"

export default function Page() {
  const [activeView, setActiveView] = useState("causation")

  const views = [
    { id: "causation", label: "Causation Chain", component: CausationChain },
    { id: "strategy", label: "Strategy Dashboard", component: StrategyDashboard },
    { id: "caselaw", label: "Case Law Matrix", component: CaseLawMatrix },
  ]

  const ActiveComponent = views.find((v) => v.id === activeView)?.component || CausationChain

  return (
    <div className="w-full min-h-screen">
      <div className="border-b bg-white p-4">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-2xl font-bold mb-4">Fenoscadia v. Kronos - Legal Analysis Dashboard</h1>
          <div className="flex gap-2">
            {views.map((view) => (
              <Button
                key={view.id}
                variant={activeView === view.id ? "default" : "outline"}
                onClick={() => setActiveView(view.id)}
              >
                {view.label}
              </Button>
            ))}
          </div>
        </div>
      </div>
      <ActiveComponent />
    </div>
  )
}
