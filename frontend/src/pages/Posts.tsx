import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import api from '../services/api'
import { Eye, Heart, MessageCircle, Share2, Bookmark } from 'lucide-react'

interface Post {
  id: string
  instagram_post_id: string
  post_type: string
  caption: string
  timestamp: string
  like_count: number
  comment_count: number
  share_count: number
  save_count: number
  reach: number
  impressions: number
  engagement_rate: number
}

const Posts: React.FC = () => {
  const { pageId } = useParams<{ pageId: string }>()
  const [posts, setPosts] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    if (pageId) {
      fetchPosts()
    }
  }, [pageId])

  const fetchPosts = async () => {
    try {
      const data = await api.getPagePosts(pageId!)
      setPosts(data)
    } catch (error) {
      console.error('Failed to fetch posts', error)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
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

  return (
    <Layout>
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="mb-6">
          <button
            onClick={() => navigate(`/dashboard/${pageId}`)}
            className="text-sm text-gray-600 hover:text-gray-900 mb-2"
          >
            ← Back to Dashboard
          </button>
          <h1 className="text-3xl font-bold text-gray-900">Posts</h1>
          <p className="mt-1 text-sm text-gray-500">
            View all posts and their performance metrics
          </p>
        </div>

        {posts.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-500">No posts found for this page</p>
            <p className="text-sm text-gray-400 mt-2">
              Posts will appear here once you sync your Instagram data
            </p>
          </div>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <ul className="divide-y divide-gray-200">
              {posts.map((post) => (
                <li key={post.id} className="px-6 py-4 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-primary-600 truncate">
                          {formatDate(post.timestamp)}
                        </p>
                        <div className="ml-2 flex-shrink-0 flex">
                          <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            {post.post_type}
                          </p>
                        </div>
                      </div>
                      {post.caption && (
                        <p className="mt-2 text-sm text-gray-700 line-clamp-2">
                          {post.caption}
                        </p>
                      )}
                      <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-6">
                        <div className="flex items-center text-sm text-gray-500">
                          <Eye className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                          <span>{post.reach.toLocaleString()}</span>
                        </div>
                        <div className="flex items-center text-sm text-gray-500">
                          <Heart className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                          <span>{post.like_count.toLocaleString()}</span>
                        </div>
                        <div className="flex items-center text-sm text-gray-500">
                          <MessageCircle className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                          <span>{post.comment_count.toLocaleString()}</span>
                        </div>
                        <div className="flex items-center text-sm text-gray-500">
                          <Share2 className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                          <span>{post.share_count.toLocaleString()}</span>
                        </div>
                        <div className="flex items-center text-sm text-gray-500">
                          <Bookmark className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                          <span>{post.save_count.toLocaleString()}</span>
                        </div>
                        <div className="flex items-center text-sm font-medium text-primary-600">
                          {(post.engagement_rate * 100).toFixed(2)}% ER
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </Layout>
  )
}

export default Posts
