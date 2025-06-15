---
title: Guide
description: Angular Guide.
---

It is recommanded to keep the version up-to-date https://angular.io/guide/updating, following the guide https://update.angular.io/.

## Installation

1. Check compatibilities of Angular/Angular-CLI, Node.js (npm is included), TypeScript and RxJS versions: https://angular.io/guide/versions or https://gist.github.com/LayZeeDK/c822cc812f75bb07b7c55d07ba2719b3. \
Install/update node version and update package versions in package.json if needed.

Recommand: `nvm` node version manager. Also mentioned in https://angular.io/guide/npm-packages
```bash
# check Node.js version
node -v
# check npm version
npm -v

# Use nvm to manage node version
# To install a specific version of node
nvm install 20.9.0
# To use a specific version of node
nvm use 20.9.0
```

2. Install dependencies for an existing project
```bash
cd ${workspace}
npm install  # --legecy-peer-deps to eliminate peer dependency error
# If fails, try
rm -r node_modules/
rm package-lock.json
npm install

# install angular cli
npm -g install @angular/cli@xx.x.x
# check globally installed
npm list -g @angular/cli

# config npm if needed
npm config set <config-name> <value>

# remove a package
npm uninstall <pacakge_name>
```
This will install required modules to the folder `node_modules`. Remember to run the command each time the npm package dependency in `package.json` is updated.

### (optional) npm configuration
```bash
# List all npm configuration settings
npm config list
# Update npm configuration in `.npmrc`.

# check npm vulnerability
npm audit
```

## Development

### Create a workspace
```bash
ng new frontend --create-application=false
```

### Create a project
```bash
ng g application virtual

# interactive selection needed
# Our choice
# SCSS
# ebable SSR and Static Site Generation

# Or
ng g app virtual --style=scss --ssr=false

ng config defaults.styleExt=scss
# if value cannot be found
ng config schematics.@schematics/angular:component.styleext scss
```
After that, the project is under frontend/projects/virtual/

### create an app
```
ng g c <app_name> --skip-tests --project=virtual
```

### Create a library
```bash
ng g library libs  # --prefix option
```

#### Create a component
```bash
ng g c <component_name> --project=libs --skip-tests

# create multiple components at a time
for i in c1 c2 c3; do ng g c shared/components/"${i}" --project=libs --skip-tests --inline-style --inline-template; done
```

#### Create a service
```bash
ng g s <service_name> --project=libs --skip-tests
```

Add export to `/libs/src/public-api.ts`.

#### Build the library
```bash
# in watch mode
ng build libs --watch

# In the library project directory, create a local npm link
npm link
```
The generated lib dist will be available in the path defined in `ng-package.json`. Add library path to `compilerOptions` -> `paths`  in `tsconfig.app.json`.

Using the library in another Project:
- Navigate to the project directory that will consume the library.
- Link the library package from the local npm registry
```bash
npm link my-shared-library
```

### Create a shared module
```bash
ng g module --project=virtual shared

# create component
ng g c shared/components/component-example --skip-tests --project=virtual --module=shared

# create service
ng g s shared/services/communication --skip-tests  --project=virtual

# create class
ng g class shared/models/model-base --skip-tests --type=model --project=virtual
```
- Add `index.ts` to shared/components/ and export to `shared.module`

### Create app module with routing
```bash
ng generate module app-module --routing --project=virtual
```

### Update styles.scss
- Add `static` folder under `src`
- Add any styling files such as `bootstrap.min.css` required to `styles` in `angular.json`

#### Troubleshooting

##### `Error: Two output files share the same path`

When using the new esbuild builder (`@angular-devkit/build-angular:application`) in Angular, there's a common issue where multiple files with the same name but from different folders can cause conflicts during the build process. For example, you might see an error like: `Error Two output files share the same path but have different contents: media/img.svg`.

This occurs because the builder tries to output files with the same name to the same location. To resolve this, add `"outputHashing": "media"` to the build options in `angular.json`. This will append a unique hash to media files, preventing naming conflicts.

##### Handling Disabled States in Angular Forms
Angular 15 introduced important changes to form disabled state handling, ensuring `setDisabledState` is always called. This fixed view-model sync issues when using `[attr.disabled]`.

**Best Practices for Reactive Forms:**
1. Create disabled controls directly: `new FormControl({ value: 'foo', disabled: true })`
2. Disable controls programmatically: `myControl.disable()` in `ngOnInit`

**Legacy Code Support:**
For Angular 15.1.0+, configure FormsModule/ReactiveFormsModule with:
`ReactiveFormsModule.withConfig({ callSetDisabledState: 'whenDisabledForLegacyCode' })`
This maintains compatibility with existing code while allowing opt-out of new behavior.


## Development server
```bash
cd ${workspace}
# IMPORTANT: build shared library first
ng build lib
# Serve 'app' project with default port: 4200
# served at http://localhost:4200/
ng serve app

# change the port to listen
ng serve app --port ${port}
```
The application will automatically reload if you change any of the source files.

## Build
```bash
cd ${workspace}
# IMPORTANT: build shared library first
ng build lib
# Default configuration is 'production'
ng build virtual
ng build --project=virtual --configuration=production
```
The build artifacts will be stored in the directory configured via the `architect/build/options/outputPath` option in `angular.json`.

    In the workspace root `tsconfig.json` file, maintain only the path mappings related to the dist directory. Specifically, ensure paths like "libs" and "libs/*" are properly mapped. This configuration helps the IDE correctly resolve and understand the code within the dist directory, preventing any error indicators in the development environment.

## Integration with Django backend

1. Set the location where built angular files to desired location
  - Modify `angular.json`
    - projects:{project}:architect:build:options:outputPath, default is `dist/...`
      We modifiy the output path under a `static` folder of an installed app. example:"abc/static/frontend/virtual".
      While in some tutorial, it directly changes the path to Django app `static` folder like "app/static"
      Note that every project needs to be modified
    - For the project with 'projectType' `library`, modify `dest` in `ng-package.json`

2. Add the built artifact directory path to `DIRS` list in Django `TEMPLATES` settings to include the path of `index.html` built from Angular

3. Add the view function in `views.py` to render the frontend `index.html`.

4. Add routing url to map the view function in `urls.py`.

5. For deployment, the `baseHref` needs to be updated to ensure the `script` tag srcs in `index.html` are using whatever url the django static app is mounted on

  - For the projects with projectType `application`, add the config projects:{project}:architect:build:configurations:production:baseHref
  `"baseHref":"/static/frontend/virtual/browser/"`, so that the built index.html static files could be found. (Since the built static files are under
  the same dir, baseHref is set as their dir path)

After the previous [Build](#build) step, you could access http://localhost:8000/path/

## Documentation Development
Use [compodoc](https://compodoc.app/) to generate documentation. The `compodoc` package is included in `package.json` as the development package, while it also can be installed via `npm install --save-dev @compodoc/compodoc@1.1.23` separately.

### How to
For local development (default port is 8080). The generated documentation is served at http://localhost:${port}/ in a watch mode:
```bash
cd ${workspace}
# for local development
npx compodoc -s -w -r ${port} -p tsconfig.doc.json
```

For deploying to a test server, after [building the angular app](#build):
```bash
# Command defined in package.json
npm run compodoc
# Or
npx compodoc -p tsconfig.doc.json
```

The folder where to store the generated documentation could be configured in `output` parameter in `.compodoc.json`.

### Features
- The customized configuration is preset and could be modified in `.compodocrc.json`.
   The info about the configuration options could be seen from [here](https://compodoc.app/guides/options.html).

- The documentation of the methods and properties of modules/components/classes/services/etc.,
  and the embedding images for visualizing the architecture of the project/modules is automatically generated.

- The code comments should be the JSDoc comments. See [JSDoc tags](https://compodoc.app/guides/jsdoc-tags.html).

- A xxx.component.md file inside the root folder of the xxx.component.ts is added inside a tab in the component page.
  It is the same for class, module etc.

- The additional documentation files written in markdown is placed in the `additional-docs/` folder, and `additional-docs/summary.json`
  explains the structure and the included files.
  The content is shown in the `Additional documentation` item of the left-side menu. More info is available [here](https://compodoc.app/guides/tips-and-tricks.html).
