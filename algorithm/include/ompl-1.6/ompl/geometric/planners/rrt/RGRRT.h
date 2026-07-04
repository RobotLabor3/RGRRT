/*********************************************************************
 * Software License Agreement (BSD License)
 *
 *  Copyright (c) 2026, XXX
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions
 *  are met:
 *
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above
 *     copyright notice, this list of conditions and the following
 *     disclaimer in the documentation and/or other materials provided
 *     with the distribution.
 *   * Neither the name of the XXX nor the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 *  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 *  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 *  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 *  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 *  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 *  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 *  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 *  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 *********************************************************************/

/* Author: XXX */

#ifndef OMPL_GEOMETRIC_PLANNERS_RGRRT_
#define OMPL_GEOMETRIC_PLANNERS_RGRRT_

#include "ompl/datastructures/NearestNeighbors.h"
#include "ompl/geometric/planners/PlannerIncludes.h"
#include "ompl/base/OptimizationObjective.h"
#include "ompl/geometric/PathSimplifier.h"

#include "ompl/geometric/planners/rrt/AORewardRRT.h"

namespace ompl
{
    namespace geometric
    {
        /** \brief Asymptotically Optimal Reward Guided RRT */
        class RGRRT : public base::Planner
        {
        public:
            /** \brief Constructor */
            RGRRT(const base::SpaceInformationPtr &si);

            ~RGRRT() override;

            void getPlannerData(base::PlannerData &data) const override;

            base::PlannerStatus solve(const base::PlannerTerminationCondition &ptc) override;

            void clear() override;

            void setup() override;

            void reset(bool solvedProblem);

            void setProblemDefinition(const base::ProblemDefinitionPtr &pdef) override;

            void setRange(double distance)
            {
                maxDistance_ = distance;
            }

            /** \brief Get the range the planner is using */
            double getRange() const
            {
                return maxDistance_;
            }

            /** \brief Get the path simplifier */
            const PathSimplifierPtr &getPathSimplifier() const
            {
                return psk_;
            }

            /** \brief Get the path simplifier */
            PathSimplifierPtr &getPathSimplifier()
            {
                return psk_;
            }

            /** \brief Attempt to simplify the current solution path. Stop computation when \e ptc becomes true at the
             * latest. */
            void simplifySolution(const base::PathPtr &p, const base::PlannerTerminationCondition &ptc);

            /** \brief Retrieve the best exact-solution cost found.*/
            ompl::base::Cost bestCost() const;

        protected:
            /** \brief The random number generator */
            RNG rng_;

            std::shared_ptr<ompl::geometric::AORewardRRT> aox_planner;

            /** \brief Free the memory allocated by this planner */
            void freeMemory();

            /** \brief The maximum length of a motion to be added to a tree */
            double maxDistance_{0.};

            double inflationFactor_{1.};

            /** \brief The instance of the path simplifier */
            PathSimplifierPtr psk_;

            base::PathPtr bestPath_{nullptr};

            ompl::base::Cost bestCost_{std::numeric_limits<double>::infinity()};

            /** \brief Objective we're optimizing */
            base::OptimizationObjectivePtr opt_;

            double initCost_;
            ompl::base::PlannerStatus solve_status;
        };
    }  // namespace geometric
}  // namespace ompl

#endif
