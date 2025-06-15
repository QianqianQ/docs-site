---
title: Learning Notes
description: Angular learning notes.
---

- Keep your codebase organized with an opinionated component model and flexible dependency injection system
- Get fast state updates with fine-grained reactivity based on Signals
- Meet your performance targets with SSR, SSG, hydration, and next-generation deferred loading (@defer)
- Guarantee everything works together with Angular's first-party modules for forms, routing, and more
- Angular DevTools
- Angular language service provides code editors with a way to get completions, errors, hints, and navigation inside Angular templates.
- Security: CCS, CSF...

## Component
Each component has three parts:
- TypeScript class
- HTML template
- CSS styles

```typescript
@Component({
  selector: 'app-root',
  template: `
    Hello Universe
  `,
  styles: `
    :host {
      color: #a144eb;
    }
  `,
  standalone: true,
  imports: [UserComponent],
})
export class AppComponent {}
```

### Component composition

```typescript
@Component({
  selector: 'app-root',
  template: `
    <section>
      <app-user />
    </section>
  `,
  standalone: true,
  imports: [UserComponent],
})
```

## Control flow

- Conditional: `@if` template syntax

```html
@if (isLoggedIn) {
    <p>test</p>
}
@else {...}

<!-- v16 or older: NgIf -->
*ngIf="exp as value" ==
<ng-template [ngIf]="exp" let-value="ngIf">
```

- Loop: `@for` template syntax

```html
@for (os of operatingSystems; track os.id) {
    {{ os.name }}
}

<!-- v16 or older: NgFor -->
<ng-template [ngFor]="exp">
*ngFor="let item of [1,2,3] as items; trackBy: myTrack; index as i" ==
<ng-template ngFor let-item [ngForOf]="[1,2,3]" let-items="ngForOf" [ngForTrackBy]="myTrack" let-i="index">
```
**Note** the use of track is required, you may use the id or some other unique identifier.

## Property binding
Set values for properties of HTML elements, Angular components and more
To bind to an element's attribute, wrap the attribute name in square brackets.

Example: `<img alt="photo" [src]="imageURL">`

## Event handling
Respond to user actions like button presses, form submissions and more
bind to events with the parentheses syntax

On a given element, wrap the event you want to bind to with parentheses and set an event handler.

Example: `<button (click)="greet()">`

## Component Communication
- Send information from a parent component to a child component: `@Input`

  Example:
  - Child app-user component: `@Input name = '';`
  - parent template: `<app-user name="Simran" />`

- Components need to communicate with parent components: `@Output`

  Use the `@Output` decorator on a class property and assign it a value of type EventEmitter.

  Example:
  - Child:
      ```
      # In component
      @Output() addItemEvent = new EventEmitter<string>();
      addItem() {
      this.addItemEvent.emit('test');  # trigger event
      }

      # In template
      <button class="btn" (click)="addItem()">Add Item</button>
      ```
  - Parent:
      ```
      <app-child (addItemEvent)="addItem($event)" />
        addItem(item: string) {
          this.items.push(item);
        }
      ```

## Deferrable Views
defer load a section of your component template.

- By default `@defer` will load the comments component when the browser is idle
- The `@placeholder` block is where you put html that will show before the deferred loading starts. The content in @placeholder blocks is eagerly loaded.
- `@loading` block is where you put html that will show while the deferred content is actively being fetched, but hasn't finished yet. The content in @loading blocks is eagerly loaded.
- Both `@placeholder` and `@loading` sections have optional parameters to prevent flickering from occurring when loading happens quickly.
    - Add a minimum duration x to the block so it will be rendered for at least x seconds.
    - loading: specify the minimum amount of time that this placeholder should be shown and amount of time to wait after loading begins before showing the loading template.
- Deferrable views have a number of trigger options. Add a viewport trigger so the content will defer load once it enters the viewport.

```html
@defer (on viewport) {
  <comments />
} @placeholder (minimum 500ms) {
    <p>test</p>
} @loading (after 100ms; minimum 1s) {
  <p>Loading comments...</p>
}
```

## Optimizing images

```
# in Component
imports: [NgOptimizedImage]

# swap out the src attribute for ngSrc, [ngSrc]
<img ngSrc="/assets/logo.svg" alt="Angular logo" width="32" height="32" />
```

**Note:** In order to prevent layout shift, the NgOptimizedImage directive requires both size attributes on each image. Or use the fill attribute to tell the image to act like a "background image", filling its containing element if could not specify width and height.  its parent element must be styled with position: "relative", position: "fixed", or position: "absolute".
```html
<div class="image-container"> // Container div has 'position: "relative"'
  <img ngSrc="www.example.com/image.png" fill />
</div>
```

One of the most important optimizations for loading performance is to prioritize any image which might be the "LCP element", which is the largest on-screen graphical element when the page loads.
```html
<img ngSrc="www.example.com/image.png" height="600" width="800" priority />
```

Optional: image loader
```
providers: [
  provideImgixLoader('https://my.base.url/'),
]

// Final URL will be 'https://my.base.url/image.png'
<img ngSrc="image.png" height="600" width="800" />
```

## Routing
```typescript
// 1. create app.routes.ts
export const routes: Routes = [
      {
    path: '',
    title: 'App Home Page',
    component: HomeComponent,
  },
];

// 2. Add routing to provider - in app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes)],
};

// 3. Import RouterOutlet in the component - in app.component.ts
imports: [RouterOutlet]

// Template for AppComponent by adding <router-outlet />
```

### Use RouterLink for Navigation
1. Import RouterLink directive
- app.component: `imports: [RouterLink, RouterOutlet],`
2. Add a routerLink to template
    ```html
    <nav>
      <a routerLink="/">Home</a>
      |
      <a routerLink="/user">User</a>
    </nav>
    <router-outlet />
    ```

## Forms
Two types of forms: template-driven and reactive

### Template-Driven
1. Create an input field

2. Import FormsModule: `component imports: [FormsModule]`

3. Add binding to the value of the input

The FormsModule has a directive called `ngModel` that binds the value of the input to a property in your class.
```html
<label for="framework">
  Favorite Framework:
  <input id="framework" type="text" [(ngModel)]="favoriteFramework" />
</label>
```

**banana box syntax [()], combines the brackets of property binding, [], with the parentheses of event binding, (), represents two-way binding: property binding and event binding.**

```typescript
@Input() childName:string;
@Output() childNameChange = new EventEmitter<string>();

// in template
[variableName]="propertyToBindTo" (variableNameChange)"propertyToBindTo=$event"
```

### Reactive
1. Import ReactiveForms module: `imports: [ReactiveFormsModule]`
2. Create the FormGroup object with FormControls
    ```typescript
    profileForm = new FormGroup({
      name: new FormControl(''),
      email: new FormControl(''),
    });
    ```
3. Link the FormGroup and FormControls to the form
  - FormGroup attaches to a form using the `[formGroup]` directive
  - FormControl can be attached with the formControlName
4. Handle update to the form
  - Access data from the formGroup `profileForm.value.name`
5. Add `ngSubmit` to the form

```html
<form [formGroup]="profileForm" (ngSubmit)="handleSubmit()">
    <input type="text" formControlName="name" />
    <input type="email" formControlName="email" />
    <button type="submit">Submit</button>
</form>
```

### Validating form
1. Import Validators
2.  Add validation to form
  ```typescript
  profileForm = new FormGroup({
    name: new FormControl('', Validators.required),
    email: new FormControl('', [Validators.required, Validators.email]),
  });
  ```
3. Check form validation in template

    FormGroup class has a valid property. You can use this property to dynamically bind attributes.

    `<button type="submit" [disabled]="!profileForm.valid">Submit</button>`

## Services
**Dependency injection (DI):** ability for Angular to provide resources you need for your application at runtime.

1. Add the `@Injectable` decorator

2. Configure the decorator

```typescript
@Injectable({
  providedIn: 'root',
})
export class CarService {}
```

## Inject-based dependency injection

Using the `inject()` function inject the CarService and assign it to a property called xxxService

```typescript
export class AppComponent {
  display = '';
  carService = inject(CarService);

  constructor() {
    this.display = this.carService.getCars().join(' â­ï¸ ');
  }
}
```

## Constructor-based dependency injection

```typescript
export class AppComponent {
  display = '';

  constructor(private carService: CarService) {
    this.display = this.carService.getCars().join(' â­ï¸ ');
  }
}
```

There are a few things to notice here:
- Use the `private` keyword
- The petCareService becomes a property you can use in your class
- The PetCareService class is the injected class

**Inject-based and Constructor-based approaches are largely the same, there are some small differences**

## Pipes
Functions that are used to transform data in templates.

1. Import pipe: `imports: [LowerCasePipe]`
2. Add the pipe to the template: `{{username | lowercase }}`

### Format data with pipes
To pass parameters to a pipe, use the : syntax followed by the parameter value.
e.g.`{{ date | date:'medium' }}`;

### Create a pipe
1. create a TypeScript class with a `@Pipe` decorator

2. Implement the transform function

    ```typescript
    @Pipe({
        standalone: true,
        name: 'reverse'
    })
    export class ReversePipe implements PipeTransform {
        transform(value: string): string {

        }
    }
    ```
3. Use the pipe in the template: `{{ word | reverse }}`

## Signals
A signal is a wrapper around a value that notifies interested consumers when that value changes. Signals can contain any value, from primitives to complex data structures. Signals may be either writable or read-only. read a signal's value by calling its getter function

- Writable signals
    ```typescript
    const count = signal(0);
    console.log('The count is: ' + count());
    count.set(3); // or
    count.update(value => value + 1);
    ```

- Computed signals: Read-only signals that derive their value from other signals. both lazily evaluated and memoized
    ```typescript
    const count: WritableSignal<number> = signal(0);
    const doubleCount: Signal<number> = computed(() => count() * 2);
    ```
- Effect: An effect is an operation that runs whenever one or more signal values change.
    ```typescript
    effect(() => {
      console.log(`The current count is: ${count()}`);
    });
    ```