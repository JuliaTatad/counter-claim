"use client"

import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card"
import { Badge } from "./components/ui/badge"

export default function CaseLawMatrix() {
  const cases = [
    {
      name: "Burlington Resources v. Ecuador",
      id: "ICSID ARB/08/5",
      similarity: 9,
      outcome: "99% of counterclaim dismissed",
      impact: "Leading authority - high standard of proof",
      strength: "Very Strong Support",
      keyFinding: "Clear and convincing evidence required for causation and damages",
      relevance: "Direct precedent for environmental counterclaims in extractive industries",
    },
    {
      name: "Urbaser v. Argentina",
      id: "ICSID ARB/07/26",
      similarity: 6,
      outcome: "Jurisdiction accepted for human rights counterclaim",
      impact: "Broadened gateway for state counterclaims",
      strength: "Significant Weakness",
      keyFinding: "Investment law allows counterclaims based on investor obligations",
      relevance: "Establishes precedent for non-commercial counterclaims",
    },
    {
      name: "Spyridon Roussalis v. Romania",
      id: "ICSID ARB/06/1",
      similarity: 4,
      outcome: "Counterclaim rejected for lack of close connection",
      impact: "Supports narrow jurisdictional interpretation",
      strength: "Strong Support",
      keyFinding: "Counterclaim must be closely connected to primary claim facts",
      relevance: "Key support for jurisdictional challenge",
    },
    {
      name: "Perenco v. Ecuador",
      id: "ICSID ARB/08/6",
      similarity: 7,
      outcome: "Partial liability found for environmental damages",
      impact: "Shows states can succeed with proper evidence",
      strength: "Key Risk",
      keyFinding: "Environmental liability possible with sufficient proof",
      relevance: "Demonstrates risk if Kronos improves evidence",
    },
    {
      name: "Paushok v. Mongolia",
      id: "UNCITRAL",
      similarity: 5,
      outcome: "Emphasized need for direct factual nexus",
      impact: "Supports jurisdictional requirements",
      strength: "Moderate Support",
      keyFinding: "Claim and counterclaim must have direct factual and legal nexus",
      relevance: "Supports argument for factual disconnect",
    },
  ]

  const getStrengthColor = (strength: string) => {
    if (strength.includes("Very Strong") || strength.includes("Strong")) return "bg-green-100 text-green-800"
    if (strength.includes("Moderate")) return "bg-yellow-100 text-yellow-800"
    if (strength.includes("Weakness") || strength.includes("Risk")) return "bg-red-100 text-red-800"
    return "bg-gray-100 text-gray-800"
  }

  const getSimilarityColor = (similarity: number) => {
    if (similarity >= 8) return "bg-green-500"
    if (similarity >= 6) return "bg-yellow-500"
    if (similarity >= 4) return "bg-orange-500"
    return "bg-red-500"
  }

  return (
    <div className="w-full min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Case Law Precedent Analysis</h1>
          <p className="text-gray-600 mt-2">Comparative analysis of relevant arbitration decisions</p>
        </div>

        <div className="grid gap-6">
          {cases.map((case_, index) => (
            <Card key={index} className="relative">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-lg">{case_.name}</CardTitle>
                    <p className="text-sm text-gray-500 mt-1">{case_.id}</p>
                  </div>
                  <div className="flex gap-2">
                    <Badge className={getStrengthColor(case_.strength)}>{case_.strength}</Badge>
                    <div className="flex items-center gap-2">
                      <span className="text-xs">Similarity:</span>
                      <div className="flex items-center gap-1">
                        <div className={`w-8 h-2 rounded ${getSimilarityColor(case_.similarity)}`}></div>
                        <span className="text-xs font-medium">{case_.similarity}/10</span>
                      </div>
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-semibold text-sm mb-1">Outcome:</h4>
                      <p className="text-sm text-gray-700">{case_.outcome}</p>
                    </div>
                    <div>
                      <h4 className="font-semibold text-sm mb-1">Key Finding:</h4>
                      <p className="text-sm text-gray-700">{case_.keyFinding}</p>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-semibold text-sm mb-1">Impact:</h4>
                      <p className="text-sm text-gray-700">{case_.impact}</p>
                    </div>
                    <div>
                      <h4 className="font-semibold text-sm mb-1">Relevance:</h4>
                      <p className="text-sm text-gray-700">{case_.relevance}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Strategic Implications</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-6 md:grid-cols-3">
              <div className="space-y-3">
                <h4 className="font-semibold text-green-700">Strongest Support</h4>
                <ul className="text-sm space-y-2">
                  <li>• Burlington's 99% dismissal rate</li>
                  <li>• High evidentiary standard precedent</li>
                  <li>• Roussalis jurisdictional test</li>
                </ul>
              </div>
              <div className="space-y-3">
                <h4 className="font-semibold text-red-700">Key Vulnerabilities</h4>
                <ul className="text-sm space-y-2">
                  <li>• Urbaser's broad jurisdiction approach</li>
                  <li>• Perenco's partial success model</li>
                  <li>• Modern tribunal trends</li>
                </ul>
              </div>
              <div className="space-y-3">
                <h4 className="font-semibold text-blue-700">Action Items</h4>
                <ul className="text-sm space-y-2">
                  <li>• Emphasize Burlington standard</li>
                  <li>• Distinguish Urbaser facts</li>
                  <li>• Secure expert testimony early</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
