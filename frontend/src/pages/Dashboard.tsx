import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import api from '../services/api'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import {
  TrendingUp,
  TrendingDown,
  Target,
  Zap,
  AlertTriangle,
  CheckCircle,
  Users,
  Eye,
  Heart,
} from 'lucide-react'

interface IntelligenceData {
  page_id: string
  instagram_username: string
  overall_score: number
  growth_stage: string
  confidence_score: number
  signals: {
    posting_consistency: number
    reach_trend: number
    conversion_health: number
    momentum: number
    engagement_stability: number
    viral_probability: number
    content_fatigue: number
  }
  recommendations: string[]
  key_metrics: {
    current_followers: number
    total_posts_analyzed: number
    total_engagement: number
    avg_engagement_rate: number
    avg_reach: number
    top_post_reach: number
  }
  analysis_period_days: number
}

const Dashboard: React.FC = () => {
  const { pageId } = useParams<{ pageId: string }>()
  const [intelligence, setIntelligence] = useState<IntelligenceData | null>(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    if (pageId) {
      fetchIntelligence()
    }
  }, [pageId])

  const fetchIntelligence = async () => {
    try {
      const data = await api.getIntelligenceScore(pageId!, 30)
      setIntelligence(data)
    } catch (error) {
      console.error('Failed to fetch intelligence', error)
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score: number): string => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-blue-600'
    if (score >= 40) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBgColor = (score: number): string => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 60) return 'bg-blue-100'
    if (score >= 40) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  const getStageIcon = (stage: string) => {
    if (stage === 'Dominant Growth') return <TrendingUp className="w-6 h-6 text-green-600" />
    if (stage === 'Stable Growth') return <CheckCircle className="w-6 h-6 text-blue-600" />
    if (stage === 'At Risk') return <AlertTriangle className="w-6 h-6 text-yellow-600" />
    return <TrendingDown className="w-6 h-6 text-red-600" />
  }

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </Layout>
    )
  }

  if (!intelligence) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-gray-500">Failed to load intelligence data</p>
        </div>
      </Layout>
    )
  }

  const signalsData = [
    { name: 'Posting', value: intelligence.signals.posting_consistency },
    { name: 'Reach', value: intelligence.signals.reach_trend },
    { name: 'Conversion', value: intelligence.signals.conversion_health },
    { name: 'Momentum', value: intelligence.signals.momentum },
    { name: 'Engagement', value: intelligence.signals.engagement_stability },
    { name: 'Virality', value: intelligence.signals.viral_probability },
  ]

  return (
    <Layout>
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="mb-6">
          <button
            onClick={() => navigate('/pages')}
            className="text-sm text-gray-600 hover:text-gray-900 mb-2"
          >
            ← Back to Pages
          </button>
          <h1 className="text-3xl font-bold text-gray-900">
            @{intelligence.instagram_username}
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Intelligence Report - Last {intelligence.analysis_period_days} days
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3 mb-6">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-6">
              <div className="flex items-center">
                <div className={`flex-shrink-0 rounded-md p-3 ${getScoreBgColor(intelligence.overall_score)}`}>
                  <Zap className={`h-8 w-8 ${getScoreColor(intelligence.overall_score)}`} />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Intelligence Score
                    </dt>
                    <dd className="flex items-baseline">
                      <div className={`text-3xl font-bold ${getScoreColor(intelligence.overall_score)}`}>
                        {intelligence.overall_score}
                      </div>
                      <div className="ml-2 text-sm text-gray-500">/100</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-primary-100 rounded-md p-3">
                  {getStageIcon(intelligence.growth_stage)}
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Growth Stage
                    </dt>
                    <dd className="text-xl font-semibold text-gray-900">
                      {intelligence.growth_stage}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-gray-100 rounded-md p-3">
                  <Target className="h-8 w-8 text-gray-600" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Confidence Score
                    </dt>
                    <dd className="text-3xl font-bold text-gray-900">
                      {intelligence.confidence_score}%
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 mb-6">
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Signal Breakdown</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={signalsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="value" fill="#0ea5e9" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Key Metrics</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <Users className="w-5 h-5 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-600">Followers</span>
                </div>
                <span className="text-lg font-semibold text-gray-900">
                  {intelligence.key_metrics.current_followers.toLocaleString()}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <Eye className="w-5 h-5 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-600">Avg Reach</span>
                </div>
                <span className="text-lg font-semibold text-gray-900">
                  {Math.round(intelligence.key_metrics.avg_reach).toLocaleString()}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <Heart className="w-5 h-5 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-600">Total Engagement</span>
                </div>
                <span className="text-lg font-semibold text-gray-900">
                  {intelligence.key_metrics.total_engagement.toLocaleString()}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <TrendingUp className="w-5 h-5 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-600">Avg Engagement Rate</span>
                </div>
                <span className="text-lg font-semibold text-gray-900">
                  {(intelligence.key_metrics.avg_engagement_rate * 100).toFixed(2)}%
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <Zap className="w-5 h-5 text-gray-400 mr-3" />
                  <span className="text-sm text-gray-600">Posts Analyzed</span>
                </div>
                <span className="text-lg font-semibold text-gray-900">
                  {intelligence.key_metrics.total_posts_analyzed}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3 mb-6">
          {Object.entries(intelligence.signals).map(([key, value]) => {
            if (key === 'content_fatigue') {
              return (
                <div key={key} className="bg-white shadow rounded-lg p-6">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-medium text-gray-900 capitalize">
                      {key.replace(/_/g, ' ')}
                    </h4>
                    <span className={`text-xl font-bold ${getScoreColor(100 - value)}`}>
                      {value.toFixed(1)}
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${value > 40 ? 'bg-red-500' : 'bg-green-500'}`}
                      style={{ width: `${value}%` }}
                    ></div>
                  </div>
                  <p className="mt-2 text-xs text-gray-500">Lower is better</p>
                </div>
              )
            }
            return (
              <div key={key} className="bg-white shadow rounded-lg p-6">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-sm font-medium text-gray-900 capitalize">
                    {key.replace(/_/g, ' ')}
                  </h4>
                  <span className={`text-xl font-bold ${getScoreColor(value)}`}>
                    {value.toFixed(1)}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      value >= 80 ? 'bg-green-500' : value >= 60 ? 'bg-blue-500' : value >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${value}%` }}
                  ></div>
                </div>
              </div>
            )
          })}
        </div>

        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Strategic Recommendations</h3>
          <div className="space-y-3">
            {intelligence.recommendations.map((rec, index) => (
              <div key={index} className="flex items-start">
                <div className="flex-shrink-0">
                  <CheckCircle className="h-5 w-5 text-green-500 mt-0.5" />
                </div>
                <p className="ml-3 text-sm text-gray-700">{rec}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-primary-50 border border-primary-200 rounded-lg p-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <Zap className="h-6 w-6 text-primary-600" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-primary-800">
                Next Steps
              </h3>
              <div className="mt-2 text-sm text-primary-700">
                <p>
                  Your {intelligence.growth_stage.toLowerCase()} status suggests focusing on{' '}
                  {intelligence.overall_score >= 60 ? 'maintaining momentum' : 'improvement areas'}.
                  Review the recommendations above and track your progress over the next 7 days.
                </p>
              </div>
              <div className="mt-4">
                <button
                  onClick={() => navigate(`/posts/${pageId}`)}
                  className="text-sm font-medium text-primary-600 hover:text-primary-500"
                >
                  View Posts →
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default Dashboard
