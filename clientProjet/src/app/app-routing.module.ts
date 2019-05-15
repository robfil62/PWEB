import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ReceptionComponent } from './reception/reception.component';
import { ResearchComponent } from './research/research.component';
import { ResultComponent } from './result/result.component';


const routes: Routes = [
  { path: '',redirectTo: '/reception', pathMatch: 'full' },
  { path: 'reception', component: ReceptionComponent },
  { path: 'research', component: ResearchComponent },
  { path: 'result', component: ResultComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
