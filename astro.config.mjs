// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'Developer Docs',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/QianqianQ' }],
			sidebar: [
				{
					label: 'Guides',
					items: [
						// Each item here is one entry in the navigation menu.
						{ label: 'Example Guide', slug: 'guides/example' },
					],
				},
				// {
				// 	label: 'Reference',
				// 	autogenerate: { directory: 'reference' },
				// },
				{
					label: 'Python',
					autogenerate: { directory: 'python' },
				},
				{
					label: 'Web Development',
					autogenerate: { directory: 'web-development' },
				},
				{
					label: 'Databases',
					autogenerate: { directory: 'databases' },
				},
				{
					label: 'Tools',
					autogenerate: { directory: 'tools' },
				},
			],
		}),
	],
});
