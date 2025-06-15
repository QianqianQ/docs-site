/*
This block contains utility functions for version comparison and extraction.
The main components are:
1. getVersions() - Extracts version components from an image name using regex
2. versionComparator - Compares two image versions based on extracted components
3. compareIntegerStrings - Helper function to compare version numbers as integers
These functions are used to sort and compare software versions in a structured way.
*/

// Function to extract version numbers given an image name
def getVersions(imageName) {
  // Extract substring containing version numbers
  def versionStr = imageName.split(/\s\-\s/)[0]
  println versionStr
  // init version numbers
  def ver1 = 0
  def ver2 = 0
  def ver3Str = ''
  def ver3Num = 0

  // Define the regular expression pattern to match the version numbers
  // def pattern = /(\d+(?:\.\d+)*)[+-]?(\d+)?(?:\-[A-Za-z]*(\d+))?/
  // Example: abc-1.0.0-1-difi100
  def pattern = /(\d+(?:\.\d+)*)[+-]?(\d+)?(?:\-([A-Za-z]*)(\d*))?/
  // regex pattern match
  def matcher = (versionStr =~ pattern)

  // Check if the first match exists
  if (matcher.find()) {
    // Extract the version numbers
    ver1 = matcher.group(1)
    ver2 = matcher.group(2)
    ver3Str = matcher.group(3)
    ver3Num = matcher.group(4)

    println ver1
    println ver1.getClass()
    println ver2
    println ver2.getClass()
    println ver3Str
    println ver3Str.getClass()
    println ver3Num
    println ver3Num.getClass()

  }

  return [ver1: ver1, ver2: ver2,
  ver3Str: ver3Str, ver3Num: ver3Num]
}

// Function to compare two image names
def versionComparator = { a, b ->
  try {
    // extract version numbers of a and b
    def versA = getVersions(a)
    def versB = getVersions(b)

    // Compare the first part of the version numbers.
    def ver1A = versA.ver1
    def ver1B = versB.ver1
    ver1A = ver1A == null ? [] : ver1A.tokenize('.')
    ver1B = ver1B == null ? [] : ver1B.tokenize('.')
    // Compare each version number from most important to least important
    def commonIndices = Math.min(ver1A.size(), ver1B.size())
    for (int i = 0; i < commonIndices; ++i) {
      def numA = ver1A[i].toInteger()
      def numB = ver1B[i].toInteger()
      if (numA != numB) {
        return numA <=> numB
      }
    }
    // If all the common indices are identical, whichever version is longer must be more recent
    if (ver1A.size() != ver1B.size()) {
      return ver1A.size() <=> ver1B.size()
    }

    // Compare verion part2
    def ver2A = versA.ver2
    def ver2B = versB.ver2
    def part2CompResult = compareIntegerStrings(ver2A, ver2B)
    if (part2CompResult != 0) {
      return part2CompResult
    }

    // Compare verion part3 str part
    def ver3StrA = versA.ver3Str == null ? '' : versA.ver3Str
    def ver3StrB = versB.ver3Str == null ? '' : versB.ver3Str
    if (ver3StrA != ver3StrB) {
      return ver3StrA.compareTo(ver3StrB)
    }

    // Compare verion part3 num part
    return compareIntegerStrings(versA.ver3Num, versB.ver3Num)
  } catch (Exception e) {
    // return as they are in the same priority if any errors occurs
    return 0
    }
}

// Function to converted two strings into integers and compare
def compareIntegerStrings(String numString1, String numString2) {
  // Init
  def number1 = 0
  def number2 = 0

  // Attempt to convert the input strings to numerical types
  try {
    number1 = numString1?.isInteger() ? numString1.toInteger() : 0
  } catch (Exception e) { }

  try {
    number2 = numString2?.isInteger() ? numString2.toInteger() : 0
  } catch (Exception e) { }

  // Perform the comparison
  return number1 <=> number2
}

// test.sort(versionComparator)
// test.reverse()
// println 'result'
// test.reverse().each { e -> println e }

//////////////////////////////////////////////////////////////////////////////////////////////////////

// This block contains two functions:
// 1. getSwReleaseVerStr - Extracts the version string from image info by splitting on '|' and spaces
// 2. versionComparator - Compares two version strings by splitting them into parts and comparing numerically

def getSwReleaseVerStr(imageInfo) {
  String swRelease = imageInfo.tokenize('|')[0]
  String swReleaseVer = swRelease.tokenize()[1]
  return swReleaseVer
}

versionComparator = { a, b ->
  try {
    // extract version numbers of a and b
    def verA = getSwReleaseVerStr(a)
    def verB = getSwReleaseVerStr(b)

    // Compare version numbers
    verPartsA = verA == null ? [] : verA.tokenize('.')
    verPartsB = verB == null ? [] : verB.tokenize('.')
    // Compare each version number from most important to least important
    def commonIndices = Math.min(verPartsA.size(), verPartsB.size())
    for (int i = 0; i < commonIndices; ++i) {
      def numA = verA[i].toInteger()
      def numB = verB[i].toInteger()
      if (numA != numB) {
        return numA <=> numB
      }
    }
    // If all the common indices are identical, whichever version is longer must be more recent
    if (verA.size() != verB.size()) {
      return verA.size() <=> verB.size()
    }

    return 0
  } catch (Exception e) {
    // return as they are in the same priority if any errors occurs
    return 0
    }
}

// Jenkins job cleanup
def jobName = "jobName"
def job = Jenkins.instance.getItem(jobName)
job.getBuilds().each { if (it.number >= 1 && it.number <= 100) it.delete() }
job.nextBuildNumber = 1
job.save()
```
Or from Linux command line
```bash
rm -rf jobs/${JOB_NAME}/builds/${BUILD_NUM}*

// Extract ID from string using regex pattern matching
str = '20250101-123456-4j3l24j2l5nmfslfjfl-xxx 1.1.0 xxx1'
str_id = ''
def id_pattern = /^[0-9]{8}-[0-9]+-[a-z0-9]+_?[A-Z0-9]*/
str_matcher = str =~ id_pattern
if (str_matcher) {
  str_id = str_matcher[0]
  println str_id
}
