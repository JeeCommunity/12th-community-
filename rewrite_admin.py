with open('src/components/AdminPanel.tsx', 'r') as f:
    content = f.read()

# Just a simple manual rewrite
content = """import { getAvatarUrl } from '../utils';
import React, { useState, useEffect } from 'react';
import { collection, query, onSnapshot, doc, updateDoc, deleteDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { UserProfile, Post } from '../types';
import { Shield, Users, Search, Ban, Trash2, ArrowLeft, Flag, ExternalLink } from 'lucide-react';

interface Props {
  onBack: () => void;
}

export function AdminPanel({ onBack }: Props) {
  const [users, setUsers] = useState<UserProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  
  const [activeTab, setActiveTab] = useState<'users' | 'reports'>('users');
  const [reportedPosts, setReportedPosts] = useState<Post[]>([]);
  
  useEffect(() => {
    if (activeTab === 'reports') {
      const q = query(collection(db, 'posts'));
      const unsub = onSnapshot(q, (snapshot) => {
        const fetched: Post[] = [];
        snapshot.forEach((doc) => {
          const post = { id: doc.id, ...doc.data() } as Post;
          if (post.reports && post.reports.length > 0) {
            fetched.push(post);
          }
        });
        fetched.sort((a, b) => (b.reportsCount || 0) - (a.reportsCount || 0));
        setReportedPosts(fetched);
      });
      return () => unsub();
    }
  }, [activeTab]);

  const handleDeletePost = async (postId: string) => {
    if (confirm('Are you sure you want to delete this reported post?')) {
      try {
        await deleteDoc(doc(db, 'posts', postId));
      } catch (err) {
        console.error('Error deleting post:', err);
      }
    }
  };
  
  const handleClearReports = async (postId: string) => {
    if (confirm('Clear all reports for this post?')) {
      try {
        await updateDoc(doc(db, 'posts', postId), { reports: [], reportsCount: 0 });
      } catch (err) {
        console.error('Error clearing reports:', err);
      }
    }
  };

  useEffect(() => {
    const q = query(collection(db, 'users'));
    const unsub = onSnapshot(q, (snapshot) => {
      const fetched: UserProfile[] = [];
      snapshot.forEach((doc) => fetched.push(doc.data() as UserProfile));
      setUsers(fetched);
      setLoading(false);
    });
    return () => unsub();
  }, []);

  const handleBlockUser = async (userId: string, isBlocked: boolean) => {
    if (confirm(`Are you sure you want to ${isBlocked ? 'unblock' : 'block'} this user?`)) {
      try {
        await updateDoc(doc(db, 'users', userId), {
          isBlocked: !isBlocked
        });
      } catch (err) {
        console.error('Error blocking user:', err);
        alert('Failed to block user. Make sure you have admin privileges.');
      }
    }
  };

  const handleDeleteUser = async (userId: string) => {
    if (confirm('Are you sure you want to completely delete this user? This cannot be undone.')) {
      try {
        await deleteDoc(doc(db, 'users', userId));
      } catch (err) {
        console.error('Error deleting user:', err);
        alert('Failed to delete user. Make sure you have admin privileges.');
      }
    }
  };

  const filteredUsers = users.filter(user => 
    user.name?.toLowerCase().includes(searchQuery.toLowerCase()) || 
    user.username?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="h-full flex flex-col bg-gray-50 overflow-hidden">
      <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between sticky top-0 z-30 shadow-sm">
        <div className="flex items-center gap-3">
          <button 
            onClick={onBack}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors text-gray-600"
          >
            <ArrowLeft size={20} />
          </button>
          <div className="flex items-center gap-2">
            <Shield className="text-red-600" size={24} />
            <h1 className="text-lg font-bold text-gray-900 leading-tight">Admin Dashboard</h1>
          </div>
        </div>
        <div className="bg-red-50 text-red-700 px-3 py-1 rounded-full text-xs font-bold border border-red-200 flex items-center gap-1.5">
          <Users size={14} />
          {users.length} Total Users
        </div>
      </div>

      <div className="flex bg-white px-4 py-2 border-b border-gray-200 sticky top-[60px] z-20 shadow-sm gap-4">
        <button
          onClick={() => setActiveTab('users')}
          className={`px-4 py-2 text-sm font-bold rounded-lg transition-colors ${activeTab === 'users' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'}`}
        >
          <div className="flex items-center gap-2"><Users size={16} /> Manage Users</div>
        </button>
        <button
          onClick={() => setActiveTab('reports')}
          className={`px-4 py-2 text-sm font-bold rounded-lg transition-colors ${activeTab === 'reports' ? 'bg-red-100 text-red-700' : 'text-gray-600 hover:bg-gray-100'}`}
        >
          <div className="flex items-center gap-2"><Flag size={16} /> Reported Posts</div>
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
        <div className="max-w-4xl mx-auto space-y-6">
          {activeTab === 'users' ? (
            <>
              <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                  <input
                    type="text"
                    placeholder="Search users by name or username..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-sm"
                  />
                </div>
              </div>

              <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                {loading ? (
                  <div className="p-8 text-center text-gray-500">Loading users...</div>
                ) : filteredUsers.length === 0 ? (
                  <div className="p-8 text-center text-gray-500">No users found.</div>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                      <thead>
                        <tr className="bg-gray-50 border-b border-gray-100">
                          <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">User</th>
                          <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Joined</th>
                          <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Status</th>
                          <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Actions</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-100">
                        {filteredUsers.map(user => (
                          <tr key={user.uid} className="hover:bg-gray-50 transition-colors">
                            <td className="px-4 py-3">
                              <div className="flex items-center gap-3">
                                <img 
                                  src={getAvatarUrl(user.photoURL, user.name)} 
                                  alt="" 
                                  className="w-10 h-10 rounded-full bg-gray-200 object-cover"
                                />
                                <div>
                                  <div className="font-semibold text-sm text-gray-900">{user.name}</div>
                                  <div className="text-xs text-gray-500">@{user.username}</div>
                                </div>
                              </div>
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-600">
                              {new Date(user.createdAt).toLocaleDateString()}
                            </td>
                            <td className="px-4 py-3">
                              {user.isBlocked ? (
                                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">
                                  Blocked
                                </span>
                              ) : (
                                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                                  Active
                                </span>
                              )}
                            </td>
                            <td className="px-4 py-3 text-right">
                              <div className="flex justify-end gap-2">
                                <button
                                  onClick={() => handleBlockUser(user.uid, !!user.isBlocked)}
                                  className={`p-1.5 rounded-lg transition-colors ${user.isBlocked ? 'bg-orange-100 text-orange-700 hover:bg-orange-200' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
                                  title={user.isBlocked ? "Unblock User" : "Block User"}
                                >
                                  <Ban size={16} />
                                </button>
                                <button
                                  onClick={() => handleDeleteUser(user.uid)}
                                  className="p-1.5 bg-red-50 text-red-600 hover:bg-red-100 rounded-lg transition-colors"
                                  title="Delete User"
                                >
                                  <Trash2 size={16} />
                                </button>
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="space-y-4">
              <h2 className="text-xl font-bold text-gray-800">Reported Posts</h2>
              {reportedPosts.length === 0 ? (
                <div className="bg-white p-8 rounded-xl border border-gray-200 text-center text-gray-500">
                  No reported posts found.
                </div>
              ) : (
                reportedPosts.map(post => (
                  <div key={post.id} className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex flex-col gap-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <img src={getAvatarUrl(post.authorPhotoURL, post.authorName)} alt="" className="w-8 h-8 rounded-full" />
                        <div>
                          <div className="font-bold text-sm text-gray-900">{post.authorName}</div>
                          <div className="text-xs text-gray-500">@{post.authorUsername}</div>
                        </div>
                      </div>
                      <div className="bg-red-100 text-red-700 text-xs font-bold px-2 py-1 rounded flex items-center gap-1">
                        <Flag size={12} /> {post.reportsCount} Reports
                      </div>
                    </div>
                    <div className="text-gray-800 text-sm whitespace-pre-wrap bg-gray-50 p-3 rounded-lg border border-gray-100">
                      {post.content}
                    </div>
                    {post.imageUrl && (
                       <img src={post.imageUrl} alt="post" className="max-h-48 rounded object-cover" />
                    )}
                    <div className="text-xs text-gray-600 bg-red-50 p-2 rounded flex-wrap">
                      <span className="font-bold">Reasons: </span>
                      {post.reports?.map(r => r.reason).join(', ')}
                    </div>
                    <div className="flex justify-end gap-2 mt-2 pt-2 border-t border-gray-100">
                      <button onClick={() => handleClearReports(post.id)} className="px-3 py-1.5 text-xs font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg">Clear Reports</button>
                      <button onClick={() => handleDeletePost(post.id)} className="px-3 py-1.5 text-xs font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg flex items-center gap-1"><Trash2 size={12}/> Delete Post</button>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
"""
with open('src/components/AdminPanel.tsx', 'w') as f:
    f.write(content)
