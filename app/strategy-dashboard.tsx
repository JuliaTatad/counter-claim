"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"

export default function StrategyDashboard() {
  const strategies = [
    {
      name: "Challenge Jurisdiction",
      strength: "Medium",
      successRate: 35,
      keyAction: "Argue lack of close connection between expropriation claim and environmental counterclaim",
      supportingCases: ["Spyridon Roussalis v. Romania", "Paushok v. Mongolia"],
      opposingCases: ["Burlington v. Ecuador", "Urbaser v. Argentina"],
      riskLevel: "medium",
      recommendation: "Argue vigorously but prepare for likely rejection",
    },
    {
      name: "Challenge Admissibility",
      strength: "Low",
      successRate: 15,
      keyAction: "Argue claim is matter for domestic courts and constitutes abuse of process",
      supportingCases: ["Chevron v. Ecuador"],
      opposingCases: ["Aven v. Costa Rica", "Urbaser v. Argentina"],
      riskLevel: "high",
      recommendation: "Weak strategy - use only as secondary argument",
    },
    {
      name: "Challenge Merits",
      strength: "High",
      successRate: 80,
      keyAction: "Focus on failure to prove causation and speculative nature of damages",
      supportingCases: ["Burlington v. Ecuador (99% dismissed)"],
      opposingCases: ["Perenco v. Ecuador"],
      riskLevel: "low",
      recommendation: "PRIMARY STRATEGY - comprehensive evidence-based rebuttal",
    },
  ]

  const getProgressColor = (rate: number) => {
    if (rate >= 70) return "bg-green-500"
    if (rate >= 40) return "bg-yellow-500"
    return "bg-red-500"
  }

  const getRiskBadgeColor = (risk: string) => {
    switch (risk) {
      case "low":
        return "bg-green-100 text-green-800"
      case "medium":
        return "bg-yellow-100 text-yellow-800"
      case "high":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  return (
    <div className="w-full min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Defense Strategy Analysis</h1>
          <p className="text-gray-600 mt-2">Fenoscadia v. Kronos - Strategic Options Assessment</p>
        </div>

        <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-3 mb-8">
          {strategies.map((strategy, index) => (
            <Card key={index} className="relative">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <CardTitle className="text-lg">{strategy.name}</CardTitle>
                  <Badge className={getRiskBadgeColor(strategy.riskLevel)}>{strategy.riskLevel} risk</Badge>
                </div>
                <CardDescription>Success Likelihood: {strategy.successRate}%</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span>Strength: {strategy.strength}</span>
                    <span>{strategy.successRate}%</span>
                  </div>
                  <Progress value={strategy.successRate} className="h-2" />
                </div>

                <div>
                  <h4 className="font-semibold text-sm mb-2">Key Action:</h4>
                  <p className="text-sm text-gray-600">{strategy.keyAction}</p>
                </div>

                <div>
                  <h4 className="font-semibold text-sm mb-2 text-green-700">Supporting Cases:</h4>
                  <ul className="text-xs text-gray-600 space-y-1">
                    {strategy.supportingCases.map((case_, idx) => (
                      <li key={idx}>• {case_}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h4 className="font-semibold text-sm mb-2 text-red-700">Opposing Cases:</h4>
                  <ul className="text-xs text-gray-600 space-y-1">
                    {strategy.opposingCases.map((case_, idx) => (
                      <li key={idx}>• {case_}</li>
                    ))}
                  </ul>
                </div>

                <div className="pt-2 border-t">
                  <h4 className="font-semibold text-sm mb-1">Recommendation:</h4>
                  <p className="text-xs text-gray-700">{strategy.recommendation}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Risk Assessment Matrix</CardTitle>
            <CardDescription>Key factors that could impact case outcome</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-3">
                <h4 className="font-semibold">High Probability Risks</h4>
                <div className="space-y-2">
                  <div className="flex justify-between items-center p-3 bg-red-50 rounded">
                    <span className="text-sm">Tribunal accepts jurisdiction (65%)</span>
                    <Badge className="bg-red-100 text-red-800">High</Badge>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-yellow-50 rounded">
                    <span className="text-sm">New evidence from Kronos</span>
                    <Badge className="bg-yellow-100 text-yellow-800">Medium</Badge>
                  </div>
                </div>
              </div>
              <div className="space-y-3">
                <h4 className="font-semibold">Success Factors</h4>
                <div className="space-y-2">
                  <div className="flex justify-between items-center p-3 bg-green-50 rounded">
                    <span className="text-sm">Inconclusive study weakness (80%)</span>
                    <Badge className="bg-green-100 text-green-800">High</Badge>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-green-50 rounded">
                    <span className="text-sm">Burlington precedent strength</span>
                    <Badge className="bg-green-100 text-green-800">High</Badge>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
