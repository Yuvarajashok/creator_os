import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import api from '../services/api'
import { Plus, TrendingUp, Users, BarChart } from 'lucide-react'

interface Page {
  id: string
  instagram_username: string
  follower_count: number
  post_count: number
  bio?: string
}

const Pages: React.FC = () => {
  const [pages, setPages] = useState<Page[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [newPageUsername, setNewPageUsername] = useState('')
  const [newPageBio, setNewPageBio] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    fetchPages()
  }, [])

  const fetchPages = async () => {
    try {
      const data = await api.getPages()
      setPages(data)
    } catch (error) {
      console.error('Failed to fetch pages', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreatePage = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await api.createPage({
        instagram_username: newPageUsername,
        bio: newPageBio,
      })
      setShowModal(false)
      setNewPageUsername('')
      setNewPageBio('')
      fetchPages()
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to create page')
    }
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
        <div className="sm:flex sm:items-center">
          <div className="sm:flex-auto">
            <h1 className="text-3xl font-bold text-gray-900">Your Pages</h1>
            <p className="mt-2 text-sm text-gray-700">
              Manage your Instagram pages and view their performance
            </p>
          </div>
          <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
            <button
              onClick={() => setShowModal(true)}
              className="inline-flex items-center justify-center rounded-md border border-transparent bg-primary-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              <Plus className="w-4 h-4 mr-2" />
              Add Page
            </button>
          </div>
        </div>

        {pages.length === 0 ? (
          <div className="text-center py-12">
            <BarChart className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No pages</h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by adding your first Instagram page.
            </p>
            <div className="mt-6">
              <button
                onClick={() => setShowModal(true)}
                className="inline-flex items-center rounded-md border border-transparent bg-primary-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary-700"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Page
              </button>
            </div>
          </div>
        ) : (
          <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {pages.map((page) => (
              <div
                key={page.id}
                className="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => navigate(`/dashboard/${page.id}`)}
              >
                <div className="p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-primary-500 rounded-md p-3">
                      <Users className="h-6 w-6 text-white" />
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-gray-500 truncate">
                          @{page.instagram_username}
                        </dt>
                        <dd className="flex items-baseline">
                          <div className="text-2xl font-semibold text-gray-900">
                            {page.follower_count.toLocaleString()}
                          </div>
                          <div className="ml-2 text-sm text-gray-500">
                            followers
                          </div>
                        </dd>
                      </dl>
                    </div>
                  </div>
                  <div className="mt-4">
                    <div className="text-sm text-gray-500">
                      {page.post_count} posts
                    </div>
                    {page.bio && (
                      <p className="mt-2 text-sm text-gray-600 line-clamp-2">
                        {page.bio}
                      </p>
                    )}
                  </div>
                  <div className="mt-4">
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        navigate(`/dashboard/${page.id}`)
                      }}
                      className="inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-500"
                    >
                      View Intelligence
                      <TrendingUp className="ml-1 w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <div className="fixed z-10 inset-0 overflow-y-auto">
          <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

            <div className="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
              <form onSubmit={handleCreatePage}>
                <div>
                  <h3 className="text-lg leading-6 font-medium text-gray-900">
                    Add Instagram Page
                  </h3>
                  <div className="mt-4">
                    <label
                      htmlFor="username"
                      className="block text-sm font-medium text-gray-700"
                    >
                      Instagram Username
                    </label>
                    <input
                      type="text"
                      id="username"
                      required
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                      placeholder="username"
                      value={newPageUsername}
                      onChange={(e) => setNewPageUsername(e.target.value)}
                    />
                  </div>
                  <div className="mt-4">
                    <label
                      htmlFor="bio"
                      className="block text-sm font-medium text-gray-700"
                    >
                      Bio (Optional)
                    </label>
                    <textarea
                      id="bio"
                      rows={3}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                      placeholder="Brief description..."
                      value={newPageBio}
                      onChange={(e) => setNewPageBio(e.target.value)}
                    />
                  </div>
                </div>
                <div className="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                  <button
                    type="submit"
                    className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:col-start-2 sm:text-sm"
                  >
                    Add Page
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:col-start-1 sm:text-sm"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </Layout>
  )
}

export default Pages
