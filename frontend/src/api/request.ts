// api/request.ts
import type { ApiResponse } from '@/types/common'

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: any
  header?: Record<string, string>
}

// H5 环境直接使用后端地址，避免被公司代理拦截
// #ifdef H5
const BASE_URL = 'http://localhost:8000/api'
// #endif

// #ifdef MP-WEIXIN
const BASE_URL = 'http://localhost:8000/api'
// #endif

export function request<T = any>(
  url: string,
  options: RequestOptions = {}
): Promise<ApiResponse<T>> {
  const { method = 'GET', data, header } = options

  // 构建 URL 和查询参数
  let fullUrl = BASE_URL + url
  if (method === 'GET' && data) {
    const params = new URLSearchParams()
    Object.keys(data).forEach(key => {
      if (data[key] !== undefined && data[key] !== null) {
        params.append(key, String(data[key]))
      }
    })
    const queryString = params.toString()
    if (queryString) {
      fullUrl += (url.includes('?') ? '&' : '?') + queryString
    }
  }

  return new Promise((resolve, reject) => {
    uni.request({
      url: fullUrl,
      method,
      data: method !== 'GET' ? data : undefined,
      header: {
        'Content-Type': 'application/json',
        ...header
      },
      success: (res: any) => {
        const response = res.data as ApiResponse<T>
        if (response.code === 0) {
          resolve(response)
        } else {
          reject(new Error(response.message || '请求失败'))
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

export const http = {
  get: <T = any>(url: string, data?: any) => request<T>(url, { method: 'GET', data }),
  post: <T = any>(url: string, data?: any) => request<T>(url, { method: 'POST', data }),
  put: <T = any>(url: string, data?: any) => request<T>(url, { method: 'PUT', data }),
  delete: <T = any>(url: string, data?: any) => request<T>(url, { method: 'DELETE', data }),
}
