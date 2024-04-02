import { RouterProvider } from '@/app/provides/RouterProvider';
import { AuthPage } from '@/pages/AuthPage';
import { ChartsPage } from '@/pages/ChartsPage';
import { CommunityPage } from '@/pages/CommunityPage';
import { ConnectionPage } from '@/pages/ConnectionPage';
import { DashboardsPage } from '@/pages/DashboardsPage';
import { ErrorPage } from '@/pages/ErrorPage';
import { FilesPage } from '@/pages/FilesPage';
import { LoginPage } from '@/pages/LoginPage';
import { PracticesPage } from '@/pages/PracticesPage';
import { WikiPage } from '@/pages/WikiPage';
import { Layout } from '@/widgets/Layout';
import { createBrowserRouter } from 'react-router-dom';

export const enum RouteApp {
	HOME = 'home',
	DASHBOARDS = 'dashboards',
	AUTH = 'auth',
	LOGIN = 'login',
	CONNECTIONS = 'connections',
	FILES = 'files',
	CHARTS = 'charts',
	WIKI = 'wiki',
	PRACTICES = 'practices',
	COMMUNITY = 'community',
}

export const RoutePath: Record<RouteApp, string> = {
	[RouteApp.HOME]: '/',
	[RouteApp.DASHBOARDS]: '',
	[RouteApp.AUTH]: '/auth',
	[RouteApp.LOGIN]: '/login',
	[RouteApp.CONNECTIONS]: 'connections',
	[RouteApp.FILES]: 'files',
	[RouteApp.CHARTS]: 'charts',
	[RouteApp.WIKI]: 'wiki',
	[RouteApp.PRACTICES]: 'practices',
	[RouteApp.COMMUNITY]: 'community',
};

export const router = createBrowserRouter([
	{
		path: RoutePath[RouteApp.AUTH],
		element: (
			<RouterProvider>
				<AuthPage />
			</RouterProvider>
		),
		errorElement: <ErrorPage />,
	},
	{
		path: RoutePath[RouteApp.LOGIN],
		element: (
			<RouterProvider>
				<LoginPage />
			</RouterProvider>
		),
		errorElement: <ErrorPage />,
	},
	{
		path: RoutePath[RouteApp.HOME],
		element: <Layout />,
		children: [
			{
				path: RoutePath[RouteApp.DASHBOARDS],
				element: (
					<RouterProvider>
						<DashboardsPage />
					</RouterProvider>
				),
				errorElement: <ErrorPage />,
			},
			{
				path: RoutePath[RouteApp.CONNECTIONS],
				element: (
					<RouterProvider>
						<ConnectionPage />
					</RouterProvider>
				),
				errorElement: <ErrorPage />,
			},
			{
				path: RoutePath[RouteApp.FILES],
				element: (
					<RouterProvider>
						<FilesPage />
					</RouterProvider>
				),
				errorElement: <ErrorPage />,
			},
			{
				path: RoutePath[RouteApp.CHARTS],
				element: (
					<RouterProvider>
						<ChartsPage />
					</RouterProvider>
				),
				errorElement: <ErrorPage />,
			},
			{
				path: RoutePath[RouteApp.WIKI],
				element: (
					<RouterProvider>
						<WikiPage />
					</RouterProvider>
				),
				errorElement: <ErrorPage />,
			},
			{
				path: RoutePath[RouteApp.PRACTICES],
				element: (
					<RouterProvider>
						<PracticesPage />
					</RouterProvider>
				),
				errorElement: <ErrorPage />,
			},
			{
				path: RoutePath[RouteApp.COMMUNITY],
				element: (
					<RouterProvider>
						<CommunityPage />
					</RouterProvider>
				),
				errorElement: <ErrorPage />,
			},
		],
		errorElement: <ErrorPage />,
	},
]);
