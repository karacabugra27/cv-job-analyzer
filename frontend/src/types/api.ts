export interface MatchAnalysis {
  uyum_puani: number
  eslesen_beceriler: string[]
  eksik_beceriler: string[]
  deneyim_uyumu: string
  genel_degerlendirme: string
}

export interface AnalysisResponse {
  id: string
  baslik: string
  tarih: string
  match: MatchAnalysis
  gelisim_onerileri: string
}

export interface HistoryItem {
  id: string
  baslik: string
  tarih: string
  uyum_puani: number | null
}

export interface HistoryList {
  items: HistoryItem[]
}
