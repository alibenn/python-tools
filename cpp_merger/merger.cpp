#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TROOT.h"
#include <mutex>
#include <thread>
#include <vector>
#include <set>
#include <string>
#include <iostream>
std::mutex mut;
size_t CopySingleTree(std::string name,std::string folder,std::vector<std::string> FileNames)
{
  mut.lock();
  TFile outfile((name+".root").c_str(),"recreate");
  TChain c((name+"/"+folder).c_str());
  c.SetMaxTreeSize(1000000000000LL); // a metric TB
  for (std::string f:FileNames)
    {
      c.AddFile(f.c_str());
    }
  mut.unlock();
  TTree * t = c.CloneTree();
  mut.lock();
  t->Write();
  outfile.Write();
  mut.unlock();
  return t->GetEntries();
}

int main(int args, char** argv)
{
  if (args < 1)
    return 1;
  ROOT::EnableThreadSafety(); 
  std::vector<std::string> FileNames(argv+1,argv+args);
  std::vector<TFile*> Files;
  std::set<std::pair<std::string,std::string> > keys;
  std::map<std::string,std::thread> threads;

  for (auto FileName: FileNames)
    {
     TFile* File = TFile::Open(FileName.c_str(),"READ");
      Files.push_back(File);
      TList * fkeys = File->GetListOfKeys();
      if (fkeys)
	for (auto key:*fkeys)
	  {
	    TDirectory * dir = (TDirectory *) File->Get(((TNamed *)key)->GetName());
	    if (dir)
	      {
		TList * fkeys2 = dir->GetListOfKeys();
		for (auto key2:*fkeys2)
		  if (keys.insert(std::pair<std::string,std::string>(((TNamed*)key )->GetName(),
								     ((TNamed*)key2)->GetName())).second)
		    threads[((TNamed*)key )->GetName()] = std::thread(CopySingleTree,
								      ((TNamed*)key )->GetName(),
								      ((TNamed*)key2)->GetName(),FileNames);
		
		
	      }
	  }
      File->Close();
    }
  //  std::cout << "survived: " << __LINE__ << std::endl; 
  
  //for (auto key:keys)
  //threads[key.first] = std::thread(CopySingleTree,key.first,key.second,FileNames);
  for (auto t=threads.begin();t!=threads.end();++t)
    t->second.join();
  /*
  for (auto key:keys)
  CopySingleTree(key.first,key.second,FileNames);
  x*/
  return 0;
}

